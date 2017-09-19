import serial
import io
import serial.tools.list_ports as list_ports

ACK_INIT = "001"
ACK_ROT = "002"
ACK_HOME = "003"
ACK_MAX = "004";
ACK_RESET = "005"


ports = list_ports.comports()
for port in ports:
    print port

device = ports[1].device
ser = serial.Serial(device, 9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
readSer = True
while True:

    while readSer:
        line = ser.readline()
        line = line[:-2]
        if line != '':
            print line

        if line == ACK_INIT:
            print 'Controller initialized'
            readSer = False
        elif line == ACK_ROT:
            print 'Rotation performed'
            readSer = False
        elif line == ACK_HOME:
            print 'Go home activated'
            readSer = False
        elif line == ACK_MAX:
            print '170 degrees reached'
            readSer = False
        elif line == ACK_RESET:
            print 'Board is reseting'
            readSer = False

    nb = raw_input('Command (0,2,6,9:exit): ')
    num = int(nb)
    if num == 0:
        ser.write(b'0')
        readSer = True
    elif num == 2:
        ser.write(b'2')
        readSer = True
    elif num == 6:
        ser.write(b'6')
        readSer = True
    elif num == 9:
        ser.write(b'2')
        ser.close()
        break



