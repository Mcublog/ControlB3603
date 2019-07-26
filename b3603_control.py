import serial
import time

debug = 0  # Print debug message
info_msg = 1  # Print info message


class Control:


    def __init__(self, port):
        self.__port = serial.Serial()
        self.__port.baudrate = 38400
        self.__port.port = port
        self.__port.timeout = 1
        self.__connection = False  # Connection property
        # Open Com
        try:
            self.__port.open()       
        except IOError:
            self.__close_connect("Can't open port")
        else:
            print("B3603 " + self.__port.port + " port is open")
            self.__connection = True     


    def __del__(self):
        self.__close_connect()
    
    
    def __iprint(self, msg: str):
        """
        Print info message 
        """
        if info_msg:
            print(msg)


    def __close_connect(self, msg: str = 'B3603 Commander stop'):
        print(msg)
        self.__connection = False
        if self.__port.is_open:
            self.__iprint("B3603 " + self.__port.port + " port close")
            self.__port.close()

    def parse_state(self, param, states):
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
                self.__close_connect("Can't write data port")
            self.__iprint('B3603 Send cmd: ' + cmd.replace('\n', ''))
            ack = self.__read_ack()
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
        
        

    def __read_ack(self):
        """
        Read B3603 ACK from port
        :return: array of strings or array with zero lenght    
        """
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
