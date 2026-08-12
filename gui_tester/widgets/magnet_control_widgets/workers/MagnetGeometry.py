import pickle


class MagnetGeometry:
    def __init__(self, magnet_data_dir):
        self.data_dir = magnet_data_dir
        self.section_1_geometry = self.load("section_1_geometry.pkl")
        self.section_2_geometry = self.load("section_2_geometry.pkl")
        self.section_3_geometry = self.load("section_3_geometry.pkl")

    def load(self, filename):
        with open(self.data_dir + filename, 'rb') as file:
            # Load the data from the file
            loaded_data = pickle.load(file)

        return loaded_data
