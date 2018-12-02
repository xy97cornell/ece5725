import serial

with serial.Serial('/dev/rfcomm0') as blue:
    msg = blue.read()

    print ("msg = " + str(msg))
