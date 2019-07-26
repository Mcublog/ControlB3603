from time import sleep
from b3603_control import Control


def close_connect(cmdr):
    del cmdr


def main():
    cmdr = Control('COM9')  # /dev/ttyUSB0 for Linux
    if cmdr.get_status() == 0:
        return close_connect(cmdr)
    
    cmdr.send_cmd("OUTPUT 0")
    sleep(1)
    cmdr.send_cmd("VOLTAGE 4200")
    cmdr.send_cmd("CURRENT 250")
    cmdr.send_cmd("OUTPUT 1")
    #sleep(5)
    #cmdr.send_cmd("OUTPUT 0")
    
    close_connect(cmdr)


if __name__ == '__main__':
    main()
