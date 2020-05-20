import serial
import time

DEBUG = 0  # Print debug message
INFO_MSG = 1  # Print info message


class Control:


    def __init__(self, port):
        self.__port = serial.Serial()
        self.__port.baudrate = 38600
        self.__port.port = port
        self.__port.timeout = 1
        self.__connection = False  # Connection property
        # Open Com
        for i in range(5):
            try:
                self.__port.open()
                self.__connection = True
                break
            except IOError:
                self.close_connect("Can't open port")
            time.sleep(.1)  # Waiting 100 ms

        if self.__connection:
            self.__connection = False
            self.__iprint("B3603 " + self.__port.port + " port is open")
            self.__connection = True # Just to send cmd
            data = self.send_cmd("STATUS")
            if data == 0:
                self.close_connect("No response")
            else:
                try:
                    output = float(self.parse_state('VIN', data))
                except:
                    self.close_connect("No response")
                    return
                self.__iprint('B3603 VIN: ' + str(output))
                self.__connection = True
        else:
            self.close_connect()


    def __del__(self):
        self.close_connect()


    def __iprint(self, msg: str):
        """
        Print info message
        """
        if INFO_MSG:
            print(msg)


    def close_connect(self, msg: str = 'B3603 Commander stop'):
        print(msg)
        self.__connection = False
        if self.__port.is_open:
            self.__iprint("B3603 " + self.__port.port + " port close")
            self.__port.close()
            return 0

    def parse_state(self, param, states):
        """
        Parse status answer
        :return: return some data from status data (example VIN, VOUT and etc)
        """
        params = ('OUTPUT', 'VIN', 'VOUT', 'COUT', 'CONSTANT', 'ACK')
        states = list(map(lambda s: s.split(), states))

        if not list(filter(lambda p: p == param, params)):
            return

        if not ':' in param:
            param = param + ':'

        for state in states:
            if param in state:
                try:
                    if (param == 'ACK:'):
                        return states[0]
                    return state[1]
                except: # States is broken
                    return
        return

    def send_cmd(self, cmd):
        """
        Send B3603 command
        :return: array of strings or array with zero lenght
        """
        ack = []
        if self.__connection == True:  # dummy protection
            if cmd.endswith('\n') == False:
                cmd = cmd + '\n'
            try:
                self.__port.write(cmd.encode())
            except:
                self.close_connect("Can't write data port")
            self.__iprint('B3603 Send cmd: ' + cmd.replace('\n', ''))
            try:
                ack = self.__read_ack()
            except:
                self.close_connect("Can't read data port")
            if debug:
                self.print_ack(ack)
        if ack:
            self.__iprint('B3603 Cmd: OK' )
        else:
            self.__iprint('B3603 Cmd: Error')
            return 0
        return ack


    def print_ack(self, data: []):
        """
        Print B3603 ACK
        """
        if data:
            print('B3603 ACK:')
            for s in data:
                print(s)


    def get_status(self):
        """
        Get connection status
        :return: true if connect
        """
        return self.__connection


    def get_port(self):
        """
        Get current port
        :return: current port
        """
        return self.__port


    def __read_ack(self):
        """
        Read B3603 ACK from port
        :return: array of strings or array with zero lenght
        """
        if self.__connection == False:
            return self.close_connect("Port is close")
        for i in range(5):  # Waiting 500 ms maximum
            if self.__port.in_waiting:
                break
            time.sleep(.1)  # Waiting 100 ms
        if self.__port.in_waiting == False:
            print('Cmd was sent, but no response')
            return
        data = []
        while self.__port.in_waiting:
            try:
                s = self.__port.readline().decode('utf-8')
            except:
                print('Data was corrupt')
                return
            s = s.replace('\r\n', '')
            data.append(s)  # Remove \r\n
        return data
