import time

from gui_tester.devices.clients.motor_client import MotorClient


class Motor:
    def __init__(self, client: MotorClient):
        self.client = client

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def send_command(self, cmd):
        resp = self.client.send_command(cmd)
        return resp

    def instant_velocity(self):

        resp = self.send_command('IV')
        # return rpm
        rpm = float(resp[5:])
        return (rpm)

    def motor_velocity(self):

        resp = self.send_command('VE')
        # return rpm
        rpm = float(resp[5:])
        return (rpm)

    def current_position(self):
        resp = self.send_command('EP')
        r = 0
        while r < 30:
            try:
                pos = float(resp[5:])
                self.last_pos = pos
                #				print ('\n ,,,,,,,Motor at:', pos)
                return pos

            except ValueError:
                #				print ('Not right')
                time.sleep(2)
                r += 1

    def set_position(self, step):

        try:
            # self.send_text('DI'+str(step))
            self.send_command('FP' + str(step))
            time.sleep(0.5)
        #			print ('Finish moving')

        except ConnectionResetError as err:
            print('*** connection to server failed: "' + err.strerror + '"')
            return False
        except ConnectionRefusedError as err:
            print('*** could not connect to server: "' + err.strerror + '"')
            return False
        except KeyboardInterrupt:
            print('\n______Halted due to Ctrl-C______')
            return False

    def stop_now(self):
        self.send_command('ST')

    def steps_per_rev(self, stepsperrev):
        self.send_command('EG' + str(stepsperrev))
        print('set stpes/rev = ' + str(stepsperrev) + '\n')

    def set_zero(self):
        self.send_command('EP0')  # Set encoder position to zero
        resp = self.client.send_command('IE')
        if int(resp[5:]) == 0:
            print('Set encoder to zero\n')
            self.client.send_command('SP0')  # Set position to zero
            resp = self.client.send_command('IP')
            if int(resp[5:]) == 0:
                print('Set current position to zero\n')
            else:
                print('Fail to set current position to zero\n')
        else:
            print('Fail to set encoder to zero\n')

    def set_acceleration(self, acceleration):
        self.send_command('AC' + str(acceleration))

    def set_deceleration(self, deceleration):
        self.send_command('DE' + str(deceleration))

    def set_speed(self, speed):
        try:
            self.send_command('VE' + str(speed))
        #			resp = self.send_text('VE')
        #			print (resp)
        except ConnectionResetError as err:
            print('*** connection to server failed: "' + err.strerror + '"')
            return False
        except ConnectionRefusedError as err:
            print('*** could not connect to server: "' + err.strerror + '"')
            return False
        except KeyboardInterrupt:
            print('\n______Halted due to Ctrl-C______')
            return False

    def check_status(self):
        # print("""
        # 	# A = An Alarm code is present (use AL command to see code, AR command to clear code)
        # 	# D = Disabled (the drive is disabled)
        # 	# E = Drive Fault (drive must be reset by AR command to clear this fault)
        # 	# F = Motor moving
        # 	# H = Homing (SH in progress)
        # 	# J = Jogging (CJ in progress)
        # 	# M = Motion in progress (Feed & Jog Commands)
        # 	# P = In position
        # 	# R = Ready (Drive is enabled and ready)
        # 	# S = Stopping a motion (ST or SK command executing)
        # 	# T = Wait Time (WT command executing)
        # 	# W = Wait Input (WI command executing)
        # 	""")
        return self.send_command('RS')

    def reset_motor(self):

        self.send_command('RE')
        print("reset motor\n")

    def inhibit(self, inh=True):
        """ inh = True:  Raises the disable line on the PWM controller to disable the output
                  False: Lowers the inhibit line
        """
        if inh:
            cmd = 'MD'
            print('motor disabled\n', sep='', end='', flush=True)
        else:
            cmd = 'ME'
            print('motor enabled\n', sep='', end='', flush=True)

        try:
            self.send_command(cmd)  # INHIBIT or ENABLE

        except ConnectionResetError as err:
            print('*** connection to server failed: "'+err.strerror+'"')
            return False
        except ConnectionRefusedError as err:
            print('*** could not connect to server: "'+err.strerror+'"')
            return False
        except KeyboardInterrupt:
            print('\n______Halted due to Ctrl-C______')
            return False

        # todo: see http://code.activestate.com/recipes/408859/  recv_end() code
        #       We need to include a terminating character for reliability, e.g.: text += '\n'
        return True

    def enable(self, en=True):
        """ en = True:  Lowers the inhibit line on the PWM controller to disable the output
                 False: Raises the inhibit line
        """
        return self.inhibit(not en)

    def set_input_usage(self, usage):
        self.send_command('SI'+str(usage))
        print('set x3 input usage to SI' + str(usage) + '\n')

