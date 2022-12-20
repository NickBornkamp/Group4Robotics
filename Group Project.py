import spike
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import math


hub = PrimeHub()
motorArm = Motor('E') # Left Motor
motorPair = MotorPair('C', 'D')
movementTimer = Timer()
color = ColorSensor('A')
#duration = 0

movementTimer.reset()
print("Ready")

# This method takes the command tuple and makes the robot perform a simple instruction
# Python Version 3.10 has a switch-case equivalent but SPIKE does not accept it.
def robotMotion(command):
    print(command[0])
    comm = command[0].upper()
    if("FORWARD" == comm):
        motorPair.move(command[1], unit = "seconds")
    elif("BACKWARD" == comm):
        motorPair.move(command[1], unit = "seconds", speed = -1*motorPair.get_default_speed())
    elif("ROTATE" == comm):
        rotate(command[1])
    elif("ARM UP" == comm):
        motorArm.run_for_seconds(seconds = command[1], speed = 10)
    elif("ARM DOWN" == comm):
        motorArm.run_for_seconds(seconds = command[1], speed = -10)
    else:
        print("ERROR: NOT VALID COMMAND")

# This method takes the stack and reverses it
def reverseCommand(stack):
    revStack = []
    for command in stack:
        comm = command[0].upper()
        if("FORWARD" == comm):
            revStack.insert(0, ("BACKWARD", command[1]))
        elif("BACKWARD" == comm):
            revStack.insert(0, ("FORWARD", command[1]))
        elif("ROTATE" == comm):
            revStack.insert(0, ("ROTATE", -1*command[1]))
        elif("ARM UP" == comm):
            revStack.insert(0, ("ARM DOWN", command[1]))
        elif("ARM DOWN" == comm):
            revStack.insert(0, ("ARM UP", command[1]))
        else:
            print("ERROR: NOT VALID COMMAND")

    return revStack

# This method rotates the robot
def rotate(degrees):
    hub.motion_sensor.reset_yaw_angle()
    turnDirection = -1 if degrees > 0 else 1
    endDegrees = min(abs(degrees), 179)
    #print(endDegrees)
    motorPair.start(steering=turnDirection * 100, speed = 40)
    while(True):
        currentDegrees = hub.motion_sensor.get_yaw_angle()
        #print(currentDegrees)
        if(abs(currentDegrees) == endDegrees):
            break
    motorPair.stop()

stackCommands = []

#stackCommands.append(("Backward", 2))
#stackCommands.append(("Rotate", 90))
#stackCommands.append(("Forward", 1))
#stackCommands.append(("Arm Up", 2))

#print(stackCommands)
#revStack = reverseCommand(stackCommands)
#print(revStack)

#for command in stackCommands:
#    robotMotion(command)
    
#for command in revStack:
#    robotMotion(command)

# This method uses the color sensor to move straight, detect an object, capture it, move it to another location, and move back to the line
def acquire_box(duration):
    motorPair.set_default_speed(25)

    color1 = color.get_reflected_light()
    print(color1)
    while(movementTimer.now() < duration):
        motorPair.start()
        wait_for_seconds(0.5)

        color2 = color.get_reflected_light()
        print(color1, color2)
        if color2 != color1:
            motorPair.stop()
            robotMotion(("Arm up", 2, 0))
            robotMotion(("Forward", 1, 25))
            robotMotion(("Arm down", 1.5, 0))

            stackCommands = []
            stackCommands.append(("Rotate", 90, 0))
            stackCommands.append(("Forward", 3, 25))

            print(stackCommands)
            revStack = reverseCommand(stackCommands)
            print(revStack)

            for command in stackCommands:
                robotMotion(command)

            robotMotion(("Arm up", 2, 0))

            for command in revStack:
                robotMotion(command)

            robotMotion(("Arm down", 1.5, 0))
            
            motorPair.start()
            robotMotion(("Forward", 1, 25))

acquire_box(30)