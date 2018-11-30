
import serial

with serial.Serial('/dev/rfcomm0') as blue:
    msg = blue.write("helllo")

    print ("msg = " + str(msg))