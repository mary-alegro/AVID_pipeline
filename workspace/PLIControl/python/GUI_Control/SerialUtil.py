import serial
import serial.tools.list_ports as list_ports

class SerialUtil:

    ACK_INIT = "001"
    ACK_ROT = "002"
    ACK_HOME = "003"
    ACK_MAX = "004"
    ACK_RESET = "005"
    ACK_LEFT = "006"
    ACK_RIGHT = "007"

    CMD_ROT = "0"
    CMD_HOME = "2"
    CMD_RESET = "6"
    CMD_LEFT = "3"
    CMD_RIGHT = "4"


    def __init__(self):
        self.ports = list_ports.comports()
        self.ser = None
        for port in self.ports:
            print port

    def get_devices(self):
        return self.ports

    def connect(self, device):
        self.ser = serial.Serial(device, 9600, timeout=1)

    def disconnect(self):
        if self.ser is not None:
            self.ser.close()


    def do_rotation(self):
        if self.ser is None:
            print "Serial connection not initialized"
            return
        self.ser.write(SerialUtil.CMD_ROT)

    def go_home(self):
        if self.ser is None:
            print "Serial connection not initialized"
            return
        self.ser.write(SerialUtil.CMD_HOME)


    def read_line(self):
        if self.ser is None:
            print "Serial connection not initialized"
            return
        line = self.ser.readline()
        line = line[:-2]
        return line