from I2C_device import *
import time
 
class Board:
    def __init__(self, addr=0x48, port=1):
        self.device = I2C_device(addr, port)
 
    def control(self):
        self.device.write_cmd(0x40)
        self.device.read()
        return self.device.read()
 
    def light(self):
        self.device.write_cmd(0x41)
        self.device.read()
        return self.device.read()
 
    def temperature(self):
        self.device.write_cmd(0x42)
        self.device.read()
        return self.device.read()
 
    def custom(self):
        self.device.write_cmd(0x43)
        self.device.read()
        return self.device.read()
 
    def output(self, val):
        self.device.write_cmd_arg(0x40, val)
 
def main():
    board = Board()
    while (1):
        print "%s: control:%d light:%d temp:%d custom:%d" % (time.asctime(),
                               board.control(),
                               board.light(),
                               board.temperature(),
                               board.custom())
        time.sleep(1)
 
if __name__ == "__main__":
    main()
