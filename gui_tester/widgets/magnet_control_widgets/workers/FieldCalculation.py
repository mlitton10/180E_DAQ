from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
import numpy as np
from scipy.interpolate import interp2d
import pickle


def calculate_magnetic_field(currents):
    with open('../data/section_1_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_1_fields = pickle.load(file)
    with open('../data/section_2_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_2_fields = pickle.load(file)
    with open('../data/section_3_fields.pkl', 'rb') as file:
        # Load the data from the file
        section_3_fields = pickle.load(file)

    with open('../data/coordinate_system.pkl', 'rb') as file:
        # Load the data from the file
        [z_space, r_space] = pickle.load(file)

    fields = [section_1_fields, section_2_fields, section_3_fields]
    total_field_br = np.zeros(section_1_fields['total']['Br'].shape)
    total_field_bz = np.zeros(section_1_fields['total']['Bz'].shape)

    for n,I in enumerate(currents):
        total_field_br += I * fields[n]['total']['Br']
        total_field_bz += I * fields[n]['total']['Bz']
    total_field = {'Br': total_field_br, 'Bz': total_field_bz}
    return total_field, [z_space, r_space]

def rungeKuttaBound(dydx, x0, y0, x_bound_low, x_bound_high, y_bound, h):
    y = y0

    y_list = [y0]
    x_list = [x0]

    while x_bound_low <= x0 <= x_bound_high and 0 <= y <= y_bound:
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * dydx(x0, y)[0]
        k2 = h * dydx(x0 + 0.5 * h, y + 0.5 * k1)[0]
        k3 = h * dydx(x0 + 0.5 * h, y + 0.5 * k2)[0]
        k4 = h * dydx(x0 + h, y + k3)[0]

        # Update next value of y
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        # Update next value of x
        x0 = x0 + h

        y_list.append(y)
        x_list.append(x0)

    return np.array(x_list), np.array(y_list)

class FieldLines:
    def __init__(self, fields, coordinate_system, n_field_lines, r_wall=0.2, stepsize=0.01):
        self.field_dict = fields
        self.Br = fields['Br']
        self.Bz = fields['Bz']

        self.coordinate_system = coordinate_system
        self.r_wall = r_wall

        field_ratio = self.Br / self.Bz

        self.ratio_interpolation = interp2d(*coordinate_system, field_ratio.T)
        self.n_field_lines = n_field_lines

        self.spatial_bounds = self._find_spatial_bounds()
        self.initial_conditions = self._pick_initial_points()
        self.stepsize= stepsize

        pass

    def _find_spatial_bounds(self):
        r_bounds = [np.min(self.coordinate_system[1]), np.max(self.coordinate_system[1])]
        z_bounds = [np.min(self.coordinate_system[0]), np.max(self.coordinate_system[0])]

        return [z_bounds, r_bounds]

    def _pick_initial_points(self):
        z_initial = self.spatial_bounds[0][0]
        r_initial = np.linspace(0, self.r_wall, self.n_field_lines)

        return np.array([(z_initial+0.001, r) for r in r_initial])

    def solveFieldLines(self, stepsize=None, initial_conditions=None):
        solutions_set = []

        if initial_conditions is None:
            for ic in self.initial_conditions:
                if stepsize is None:
                    z_sol, r_sol = rungeKuttaBound(self.ratio_interpolation, ic[0], ic[1], self.spatial_bounds[0][0],
                                                  self.spatial_bounds[0][1], self.spatial_bounds[1][1], self.stepsize)
                else:
                    z_sol, r_sol = rungeKuttaBound(self.ratio_interpolation, ic[0], ic[1], self.spatial_bounds[0][0],
                                                   self.spatial_bounds[0][1], self.spatial_bounds[1][1], stepsize)
                solutions_set.append((z_sol, r_sol))

        else:
            for ic in initial_conditions:
                if stepsize is None:
                    z_sol, r_sol = rungeKuttaBound(self.ratio_interpolation, ic[0], ic[1], self.spatial_bounds[0][0],
                                                  self.spatial_bounds[0][1], self.spatial_bounds[1][1], self.stepsize)
                else:
                    z_sol, r_sol = rungeKuttaBound(self.ratio_interpolation, ic[0], ic[1], self.spatial_bounds[0][0],
                                                   self.spatial_bounds[0][1], self.spatial_bounds[1][1], stepsize)
                solutions_set.append((z_sol, r_sol))
        return solutions_set


class FieldCalculationWorker(QObject):
    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    @pyqtSlot(float, float, float)
    def calculate(self, current):
        try:
            total_field, coords = calculate_magnetic_field(current)
            field_line_solver = FieldLines(total_field, coords, 10)
            cathode_z_displacement = -158 * 1e-3
            cathode_radius = 0.078
            solutions = field_line_solver.solveFieldLines()
            solution_cathode = field_line_solver.solveFieldLines(stepsize=-0.01, initial_conditions=[
                (3.45 + cathode_z_displacement - 0.3, 0.075)])
            self.finished.emit([total_field, solutions, solution_cathode])
        except Exception as exc:
            self.failed.emit(str(exc))