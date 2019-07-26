from time import sleep
from b3603_control import Control


def close_connect(cmdr):
    del cmdr


def main():
    cmdr = Control('COM9')  # /dev/ttyUSB0 for Linux
    if cmdr.get_status() == 0:
        return close_connect(cmdr)
    
    cmdr.send_cmd("OUTPUT 0")    
    close_connect(cmdr)


if __name__ == '__main__':
    main()
