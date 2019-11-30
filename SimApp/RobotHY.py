import random
import os
import sys
import time

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class Robot(EasyPygame.Components.GameObject):
    def __init__(self, scene, rect=(0, 0), position=[0, 0, 0], name='Robot', increment=100,
    errorRate=0.05, delay=0):
        super().__init__(scene, name)
        self.position = position
        self.increment = increment
        self.errorRate = errorRate
        self.errorNumSteps = [0, 2]
        self.updateRect()
        self.delay = delay
        self.rect.x = rect[0]
        self.rect.y = rect[1]
        
        
        self.robot_TV_checking = self.addTextureView(EasyPygame.Components.TextureView("RobotChecking.png"))
        self.robot_TV_moving = self.addTextureView(EasyPygame.Components.TextureView("RobotMoving.jpg"))
        self.robot_TV_stopped = self.addTextureView(EasyPygame.Components.TextureView("RobotStopped.jpg"))
        self.useTextureView(self.robot_TV_stopped)

    #decides the number of steps Robot will take.
    def failureSimulation(self):
        #the robot will take one step with probability 1 - errorRate.
        if random.random() > self.errorRate:
            return 1
        #the robot will take 0 or 2 steps with probability errorRate.
        else:
            return random.choice(self.errorNumSteps)
            
    def setLocation(self, loc):
        self.position[0] = loc[0]
        self.position[1] = loc[1]

    def move(self):
        
        x = self.position[0]
        y = self.position[1]
        direction = self.position[2]

        numSteps = self.failureSimulation()
        if direction == 0:
            y += numSteps
        elif direction == 1:
            x += numSteps
        elif direction == 2:
            y -= numSteps
        elif direction == 3:
            x -= numSteps
        #self.pygame.time.get_fps()
        
        self.setCoordinates(x, y)
        
        self.updateRect()
        #self.useTextureView(self.robot_TV_moving)
        #EasyPygame.pygame.time.delay(500)
        EasyPygame.pygame.time.delay(self.delay)
        #self.useTextureView(self.robot_TV_stopped)
    
    def location(self):
        return [self.position[0], self.position[1]]

    def direction(self):
        return self.position[2]

    def setCoordinates(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def rotate(self):
        #self.useTextureView(self.robot_TV_moving)
        EasyPygame.pygame.time.delay(self.delay)
        self.position[2] = (self.position[2] + 1) % 4
        #self.useTextureView(self.robot_TV_stopped)     

    def getPos(self):
        self.useTextureView(self.robot_TV_checking)
        EasyPygame.pygame.time.delay(self.delay)
        self.useTextureView(self.robot_TV_stopped)
        return self.position

    def senseHazard(self):
        self.useTextureView(self.robot_TV_checking)
        EasyPygame.pygame.time.delay(self.delay)
        self.useTextureView(self.robot_TV_stopped)

    def senseBlob(self):
        self.useTextureView(self.robot_TV_checking)
        EasyPygame.pygame.time.delay(self.delay)
        self.useTextureView(self.robot_TV_stopped)
        
    def updateRect(self):
        x = self.position[0]
        y = self.position[1]
        self.rect.x = self.increment * x
        self.rect.y = self.increment * y

class Checking(EasyPygame.Components.GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(1)




# TEST

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class wentLeft(EasyPygame.Components.GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(0)

class wentRight(EasyPygame.Components.GameObjectState):
    def onEnter(self, gameObject, ms):
        gameObject.useTextureView(1)

class robotHandler(EasyPygame.Components.InputHandler):
    def update(self, gameObject, ms):
        if EasyPygame.isDown1stTime("d"):
            gameObject.FSM.switchState(1, ms)
        elif EasyPygame.isDown1stTime("r"):
            gameObject.rotate()
        elif EasyPygame.isDown1stTime("h"): 
            gameObject.senseHazard()
        elif EasyPygame.isDown1stTime("b"):
            gameObject.senseBlob()
        elif EasyPygame.isDown1stTime("p"):
            EasyPygame.loadScene("Scene2")
            EasyPygame.switchScene("Scene2")
            EasyPygame.unloadScene("Scene1")
        elif EasyPygame.isDown1stTime(" "):
            gameObject.move()

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.carrot = None
        self.testObj1 = None
        self.testObj2 = None

        self.testObj1 = EasyPygame.Components.GameObject(self, "Test1")
        self.testObj1.rect.x = 100
        self.testObj1.z = -1
        self.testObj1.useInputHandler(1)
        self.testObj1.FSM.addState(wentLeft())
        self.testObj1.FSM.addState(wentRight())

        self.robot = Robot(self, errorRate=0.0)
        self.robot.addInputHandler(robotHandler())
        self.robot.useInputHandler(1)
        #self.robot.FSM.attachAnimationState(0, EasyPygame.Components.SpriteAnimState(1000, [1, 2, 3]))
        #self.robot.FSM.addState(EasyPygame.Components.GameObjectState(1, 0))

    def onLoad(self):
        EasyPygame.load('RobotChecking.png')
        EasyPygame.load('RobotMoving.jpg')
        EasyPygame.load('RobotStopped.jpg')

    def unLoad(self):
        EasyPygame.unload("Carrot.jpg")
        EasyPygame.unload('RobotChecking.png')
        EasyPygame.unload('RobotMoving.jpg')
        EasyPygame.unload('RobotStopped.jpg')

class Scene2(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()

    def postRender(self):
        EasyPygame.pprint("this is scene2", 0, 0)

if __name__ == "__main__":
    EasyPygame.initWindow(800, 800, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
