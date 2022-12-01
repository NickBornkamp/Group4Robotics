import spike
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math


hub = PrimeHub()
motorArm = Motor('E') # Left Motor
motorPair = MotorPair('C', 'D')
movementTimer = Timer()
duration = 0


movementTimer.reset()
print("Ready")

def testArm():
    motorArm.start(speed = 10)
    while(movementTimer.now() < duration):
        motorArm.set_degrees_counted(0)
        degreesThen = motorArm.get_degrees_counted()
        wait_for_seconds(0.2)
        degreesNow = motorArm.get_degrees_counted()

        degDiff = abs(degreesNow - degreesThen)
        print(degDiff)
        if(degDiff < 15):
            motorArm.start(speed = motorArm.get_speed()*-1)
    motorArm.stop()


def robotMotion(command):
    if("Forward" == command[0]):
        motorPair.move(command[1], unit = "seconds")
    elif("Backward" == command[0]):
        motorPair.move(command[1], unit = "seconds", speed = -1*motorPair.get_default_speed())
    elif("Spin" == command[0]):
        motorPair.move(command[1], unit = "degrees", steering = 100)
    elif("Arm" == command[0]):
        motorArm.run_for_seconds(seconds = command[1], speed = 10)
    else:
        print("ERROR: NOT VALID COMMAND")
    

def spin(degrees):
    motorPair.move(4.25 * degrees * (math.pi/360), 'in', steering=100)

    spin(180)



robotMotion(("Forward", 4))
robotMotion(("Backward", 2))
robotMotion(("Spin", 180))
robotMotion(("Arm", 1))
