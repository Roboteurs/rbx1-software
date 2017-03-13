
from inputs import get_gamepad
import RPi.GPIO as GPIO
import Slush
import math
import time


#setup all of the axis for the SlushEngine
b = Slush.sBoard()
joints = [Slush.Motor(4), Slush.Motor(5), Slush.Motor(0), Slush.Motor(1), Slush.Motor(2), Slush.Motor(3)]

#reset the joints to clear previous errors
for joint in joints:
    joint.resetDev()
    joint.setMicroSteps(16)

#some initalization stuff that needs cleanup
joints[0].setMaxSpeed(150)
joints[1].setMaxSpeed(150)
joints[2].setMaxSpeed(250)
joints[3].setMaxSpeed(150)
joints[4].setMaxSpeed(150)
joints[5].setMaxSpeed(150)

#joint current limits. Still setting manually becuase testing
joints[0].setCurrent(75, 75, 75, 75)
joints[1].setCurrent(65, 65, 65, 65)
joints[2].setCurrent(50, 50, 50, 50)
joints[3].setCurrent(75, 75, 75, 75)
joints[4].setCurrent(95, 95, 95, 95)
joints[5].setCurrent(65,65, 65, 65)

#setup the gripper
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)


def waitForRobot():
    for joint in joints:
        while joint.isBusy(): continue

def robotMove(speed, points):
    
    #wait for the robot to stop doing things
    for joint in joints:
        while joint.isBusy(): continue
            
    #get the current location of the robot
    currentpos = []
    for joint in joints:
        currentpos.append(joint.getPosition())
    
    #make a list of the difference
    differencepose = [points - currentpos for points, currentpos in zip(points, currentpos)]
    maxmove = (max(map(abs, differencepose)))
    i = 0
    for joint in joints:
        try:
            jointspeed = speed * (abs(differencepose[i])/maxmove)
        except:
            jointspeed = 1
        if jointspeed < 1: jointspeed = 1
        joint.setMaxSpeed(math.ceil(jointspeed))
        joint.setMinSpeed(0)
        joint.goTo(int(points[i]))
        i = i + 1


def moveFilePoint(name):
    if name == "LIST":
        with open("example/points.ini") as pointfile:
            for line in pointfile:
                print (line)
    with open("example/points.ini") as pointfile:
        namesfound = 0
        for line in pointfile:
            if line.startswith(name):
                namesfound = 1
                points = line.split(':')
                if points[0] == name:
                    intpoints = []
                    for point in points[1:len(points)]:
                        intpoints.append(int(point))
                    robotMove(80, intpoints)                                
    if not namesfound: print("Point Data not Found")

def runProgram():
    with open("example/run.rbt") as programfile:
        i = 0
        for line in programfile:
            print("N" + str(i) + ":" + line)
            i += 1
            lineinfo = line.rstrip('\n').split(' ')
            if lineinfo[0] == "GOTO":
                moveFilePoint(lineinfo[1])
            if lineinfo[0] == "SLEEP":
                waitForRobot()
                time.sleep(int(lineinfo[1]))
            if lineinfo[0] == "GRIPPER":
                waitForRobot()
                if lineinfo[1] == "OPEN":
                    pwm.start(7)
                if lineinfo[1] == "CLOSE":
                    pwm.start(17)
            if lineinfo[0] == "EXIT":
                break

#start reading the inputs from the gamepad and putting them out the joints
gripper = 7
while 1:
    events = get_gamepad()
    for event in events:
        if event.code == 'BTN_MODE':
            value = event.state
            if value == 1:
                for joint in joints:
                    joint.free()
        
        if event.code == 'ABS_X':
            value = event.state
            if value < -1500:
                if not joints[0].isBusy(): joints[0].run(1, 35)
            elif value > 5000:
                if not joints[0].isBusy(): joints[0].run(0, 35)
            else:
                if not joints[0].isBusy(): joints[0].softStop()
        if event.code == 'ABS_Y':
            value = event.state
            if value < -1500:
                if not joints[1].isBusy(): joints[1].run(1, 20)
            elif value > 5000:
                if not joints[1].isBusy(): joints[1].run(0, 20)
            else:
                if not joints[1].isBusy(): joints[1].softStop()
        if event.code == 'ABS_RX':
            value = event.state
            if value < -3500:
                if not joints[2].isBusy(): joints[2].run(1, 100)
            elif value > 3500:
                if not joints[2].isBusy(): joints[2].run(0, 100)
            else:
                if not joints[2].isBusy(): joints[2].softStop()
        if event.code == 'ABS_RY':
            value = event.state
            if value < -3500:
                if not joints[3].isBusy(): joints[3].run(1, 10)
            elif value > 3500:
                if not joints[3].isBusy(): joints[3].run(0, 10)
            else:
                if not joints[3].isBusy(): joints[3].softStop()
        if event.code == 'ABS_HAT0Y':
            value = event.state
            if value == 1:
                if not joints[4].isBusy(): joints[4].run(1, 20)
            elif value == -1:
                if not joints[4].isBusy(): joints[4].run(0, 20)
            else:
                if not joints[4].isBusy(): joints[4].softStop()
        if event.code == 'ABS_HAT0X':
            value = event.state
            if value == 1:
                if not joints[5].isBusy(): joints[5].run(1, 20)
            elif value == -1:
                if not joints[5].isBusy(): joints[5].run(0, 20)
            else:
                if not joints[5].isBusy(): joints[5].softStop()
        if event.code == 'BTN_TL':
            if event.state == 1:
                gripper = gripper - 1
                if gripper < 7:
                    gripper = 7
                pwm.start(gripper)
        if event.code == 'BTN_TR':
            if event.state == 1:
                gripper = gripper + 1
                if gripper > 17:
                    gripper = 17
                pwm.start(gripper)
        #calibrate all axis if on point
        if event.code == 'BTN_START':
            if event.state == 1:
                for joint in joints:
                    joint.setAsHome()
        if event.code == 'BTN_SOUTH':
            if event.state == 1:
                print ("no function")
        if event.code == 'BTN_NORTH':
            if event.state == 1:
                runProgram()
        if event.code == 'BTN_EAST':
            if event.state == 1:
                name = input('Name Point (no spaces): ')
                if name == 'EXIT': break
                with open("example/points.ini", "a") as pointfile:
                    for joint in joints:
                        name += (':'+str(joint.getPosition()))
                    name +=(':' + str(gripper))
                    name +=('\n')
                    pointfile.write(name)
        if event.code == 'BTN_WEST':
            if event.state == 1:
                name = input('Go To Point (no spaced): ')
                moveFilePoint(name)
