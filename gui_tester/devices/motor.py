import time

from gui_tester.devices.clients.motor_client import MotorClient


class Motor:
    def __init__(self, client: MotorClient):
        self.client = client

    def instant_velocity(self):

        resp = self.client.send_command('IV')
        # return rpm
        rpm = float(resp[5:])
        return (rpm)

    def motor_velocity(self):

        resp = self.client.send_command('VE')
        # return rpm
        rpm = float(resp[5:])
        return (rpm)

    def current_position(self):
        resp = self.client.send_command('EP')
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
            self.client.send_command('FP' + str(step))
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
        self.client.send_command('ST')

    def steps_per_rev(self, stepsperrev):
        self.client.send_command('EG' + str(stepsperrev))
        print('set stpes/rev = ' + str(stepsperrev) + '\n')

    def set_zero(self):
        self.client.send_command('EP0')  # Set encoder position to zero
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
        self.client.send_command('AC' + str(acceleration))

    def set_decceleration(self, decceleration):
        self.client.send_command('DE' + str(decceleration))

    def set_speed(self, speed):
        try:
            self.client.send_command('VE' + str(speed))
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
