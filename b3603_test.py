from time import sleep
import datetime


from b3603_control import Control


def log_cmd(func):
    def wrapper(arg):
        f = open('log.txt', 'a')
        f.write(str(datetime.datetime.now()) + '\n')
        f.write('Send cmd: ' + arg + '\n')
        ret = func(arg);
        if (ret):
            f.write('Send cmd: OK\r\n')
        else:
            f.write('Send cmd: Fail\r\n')
        f.close();
        return ret
    return wrapper;

def parse_state(param, states):
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

def close_connect(cmdr):
    del cmdr

def main():
    cmdr = Control('COM9')  # /dev/ttyUSB0 for Linux
    if cmdr.get_status() == 0:
        return close_connect(cmdr)
        
    cmdr.send_cmd = log_cmd(cmdr.send_cmd);
    
    if cmdr.send_cmd("VOLTAGE 3300") == 0:
        return close_connect(cmdr)
    if cmdr.send_cmd("OUTPUT 1") == 0:
        return close_connect(cmdr)
    # sleep(5)
    if cmdr.send_cmd("OUTPUT 0") == 0:
        return close_connect(cmdr)

    data = cmdr.send_cmd("STATUS")
    if data == 0:
        return close_connect(cmdr)        
    print(data)        
    close_connect(cmdr)

    # states = list(map(lambda s: s.split(), data))
    # print(states)
    output = cmdr.parse_state('VOUT', data)
    if output:
        print(output)    


if __name__ == '__main__':
    main()
