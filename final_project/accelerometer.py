import logging
import sys
import time

from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

is_calibrating = False
zero_heading = 0
zero_roll = 0
zero_pitch = 0
bno = 0

def GPIO17_callback(channel):
    """
    interrupt handler for GPIO17; button on piTFT
    """
    print ("in interrupt 17")
    global is_calibrating
    is_calibrating = not is_calibrating

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

def calibrate(bno):
    print("CALIBRATING")
    global zero_heading, zero_roll, zero_pitch
    while (is_calibrating):
        print("CALIBRATING")
        #bno.set_calibration(bno.get_calibration())
        
        zero_heading, zero_roll, zero_pitch = bno.read_euler()
        sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.
        print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
              zero_heading, zero_roll, zero_pitch, sys, gyro, accel, mag))
        time.sleep(1)
    
    
def bno_init():
    global bno
    bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

    #if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
     #   logging.basicConfig(level=logging.DEBUG)
    while True:
        try:
            if not bno.begin():
                raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')    
            status, self_test, error = bno.get_system_status()
            break
        except Exception as e:
            print("error :{}".format(e))
            time.sleep(0.5)
        
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))
        print('See datasheet section 4.3.59 for the meaning.')

    # Print BNO055 software revision and other diagnostic data.
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    print('Accelerometer ID:   0x{0:02X}'.format(accel))
    print('Magnetometer ID:    0x{0:02X}'.format(mag))
    print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
        

def bno_poll():
    if is_calibrating:
        calibrate(bno)
    
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
         # heading, roll, pitch, sys, gyro, accel, mag))
    D_H = heading-zero_heading
    D_R = roll-zero_roll
    D_P = pitch-zero_pitch
    #print ("D_H = {0:0.2F} D_R = {1:0.2F} D_P={2:0.2F}".format(
    #D_H, D_R, D_P))
    return (D_H, D_R, D_P)


if __name__ == '__main__':
	
    
    while True:
        bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

        #if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
         #   logging.basicConfig(level=logging.DEBUG)
        while True:
            try:
                if not bno.begin():
                    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')    
                status, self_test, error = bno.get_system_status()
                break
            except Exception as e:
                print("error :{}".format(e))
                time.sleep(0.5)
            
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

        # Print BNO055 software revision and other diagnostic data.
        sw, bl, accel, mag, gyro = bno.get_revision()
        print('Software version:   {0}'.format(sw))
        print('Bootloader version: {0}'.format(bl))
        print('Accelerometer ID:   0x{0:02X}'.format(accel))
        print('Magnetometer ID:    0x{0:02X}'.format(mag))
        print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
        try:
            while True:
                # Read the Euler angles for heading, roll, pitch (all in degrees).
                heading, roll, pitch = bno.read_euler()
                # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
                sys, gyro, accel, mag = bno.get_calibration_status()
                # Print everything out.
                print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
                      heading, roll, pitch, sys, gyro, accel, mag))
                D_H = heading-zero_heading
                D_R = roll-zero_roll
                D_P = pitch-zero_pitch
                print ("D_H = {0:0.2F} D_R = {1:0.2F} D_P={2:0.2F}".format(
                D_H, D_R, D_P))
                if (D_R > 20):
                    print ("LEFT")
                elif (D_R < -20):
                    print ("RIGHT")
                else: 
                    print ("FORWARD")
                
                
                if is_calibrating:
                    calibrate(bno)

                time.sleep(1)    
        except Exception as e:
            print("error :{}".format(e))
