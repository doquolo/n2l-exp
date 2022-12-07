import time
import serial
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
ports = sorted(ports)

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

i = int(input("Select COM port to listen: "))
ser = serial.Serial(str(ports[i-1].name), 9600, timeout=0.050)
print(ser.in_waiting)
while True:
    if (ser.in_waiting != 0):
        sout = ser.readline()
        print("Received string: ",sout, "\n")
        sout_decoded = str(sout).split(";")
        print("Decoded string: ", sout_decoded, "\n")
    else:
        print(".", end=" ")
