import serial

with serial.Serial('/dev/rfcomm0') as blue:
    msg = blue.read(100)

    print ("msg = " + str(msg))
