import random
import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame

class Robot(EasyPygame.Components.GameObject):
    def __init__(self, scene, position=(0, 0), name='Robot', increment=100,
    errorRate=0.05):
        super().__init__(scene, name)
        self.direction = 0
        self.position = position
        self.increment = increment
        self.errorRate = errorRate
        self.errorNumSteps = [0, 2]
        self.updateRect()

        EasyPygame.load('RobotChecking.png')
        EasyPygame.load('RobotMoving.jpg')
        EasyPygame.load('RobotStopped.jpg')
        
        self.robot_TV_checking = self.addTextureView(EasyPygame.Components.TextureView("checking"))
        self.robot_TV_moving = self.addTextureView(EasyPygame.Components.TextureView("moving"))
        self.robot_TV_stopped = self.addTextureView(EasyPygame.Components.TextureView("stopped"))
        self.useTextureView(self.robot_TV_checking)

    #decides the number of steps Robot will take.
    def failureSimulation(self):
        #the robot will take one step with probability 1 - errorRate.
        if random.random() > self.errorRate:
            return 1
        #the robot will take 0 or 2 steps with probability errorRate.
        else:
            return random.choice(self.errorNumSteps)

    def move(self):
        x = self.position[0]
        y = self.position[1]
        
        numSteps = self.failureSimulation()
        if self.direction == 0:
            y += numSteps
        elif self.direction == 1:
            x += numSteps
        elif self.direction == 2:
            y -= numSteps
        elif self.direction == 3:
            x -= numSteps
        
        self.setCoordinates(x, y)
        self.updateRect()

    def setCoordinates(self, x, y):
        self.postion[0] = x
        self.postion[1] = y

    def rotate(self):
        self.position[2] = (self.position[2] + 1) % 4        

    def getPos(self):
        return self.position

    def senseHazard(self):
        pass

    def senseBlob(self):
        pass

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
            gameObject.rect.x += 100
        elif EasyPygame.isDown1stTime("a"):
            gameObject.rect.x -= 100
        elif EasyPygame.isDown1stTime("w"):
            gameObject.rect.y += 100
        elif EasyPygame.isDown1stTime("s"):
            gameObject.rect.y -= 100
        elif EasyPygame.isDown1stTime("p"):
            EasyPygame.loadScene("Scene2")
            EasyPygame.switchScene("Scene2")
            EasyPygame.unloadScene("Scene1")

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

        self.robot = Robot(self)
        self.robot.addInputHandler(robotHandler())
        self.robot.useInputHandler(1)

    def unUnload(self):
        EasyPygame.unload("Carrot.jpg")

class Scene2(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()

    def postRender(self):
        EasyPygame.pprint("this is scene2", 0, 0)

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()
