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
        spin(command[1])
    elif("Arm Up" == command[0]):
        motorArm.run_for_seconds(seconds = command[1], speed = 10)
    elif("Arm Down" == command[0]):
        motorArm.run_for_seconds(seconds = command[1], speed = -10)
    else:
        print("ERROR: NOT VALID COMMAND")
    

def spin(degrees):
    hub.motion_sensor.reset_yaw_angle()
    turnDirection = -1 if degrees > 0 else 1
    endDegrees = min(abs(degrees), 179)
    #print(endDegrees)
    motorPair.start(steering=turnDirection * 100, speed = 40 * turnDirection)
    while(True):
        currentDegrees = hub.motion_sensor.get_yaw_angle()
        #print(currentDegrees)
        if(abs(currentDegrees) == endDegrees):
            break
    motorPair.stop()


            

print("Testing 90 degrees")
wait_for_seconds(1)
robotMotion(("Spin", 90))

print("Testing 180 degrees")
wait_for_seconds(1)

robotMotion(("Spin", 180))

print("Testing -90 degrees")
wait_for_seconds(1)

robotMotion(("Spin", -90))
