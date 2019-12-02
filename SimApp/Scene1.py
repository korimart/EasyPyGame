import os, sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *
import ast
from SimApp.Scene2 import Scene2

class Scene1(Scene):
    ERRORMESSAGETIME = 2000
    def __init__(self):
        super().__init__()
        self.inputFields = []
        self.submitButton = None
        self.errorMessage = ""
        self.errorMessageTime = 0

    def onLoad(self):
        EasyPygame.load("animated.png")
        data = ["20x20", "0,0", "[(19, 19)]", "[(1,0), (0, 1)]"]
        for i in range(4):
            inputField = GUI.TextBox(self, name="input" + str(i), defaultText=data[i])
            inputField.setX(-1)
            inputField.setY(2 - i * 1.2)
            inputField.setWidth(3)
            self.inputFields.append(inputField)

        self.submitButton = GUI.Button(self, name="Submit", callback=lambda: self.checkInput())
        self.submitButton.rect.x = 1.5
        self.submitButton.rect.y = -1

    def postRender(self, ms):
        if self.errorMessage and not self.errorMessageTime:
            self.errorMessageTime = self.ERRORMESSAGETIME

        if self.errorMessage:
            EasyPygame.pprint(self.errorMessage, 0, 450, False, (255, 0, 0))
            self.errorMessageTime -= ms
        if self.errorMessageTime < 0:
            self.errorMessageTime = 0
            self.errorMessage = ""

    def checkInput(self):
        inputs = [inputField.getText() for inputField in self.inputFields]

        # width by height
        for separator in ["x", "X"]:
            widthAndHeight = inputs[0].split(separator)
            if len(widthAndHeight) == 2:
                break

        if len(widthAndHeight) != 2:
            self.errorMessage = "only width and height must be given"
            return

        try:
            width = ast.literal_eval(widthAndHeight[0])
            height = ast.literal_eval(widthAndHeight[1])
            assert type(width) is int and type(height) is int
            assert width > 0 and height > 0
        except:
            self.errorMessage = "Incorrect width and/or height"
            return

        try:
            startPos = ast.literal_eval(inputs[1])
            assert type(startPos) is tuple
            assert type(startPos[0]) is int and type(startPos[1]) is int
            assert 0 <= startPos[0] < width and 0 <= startPos[0] < height
        except:
            self.errorMessage = "Incorrect Starting Locations"
            return

        try:
            targetPosList = ast.literal_eval(inputs[2])
            assert type(targetPosList) is tuple or type(targetPosList) is list
            for pos in targetPosList:
                assert type(pos) is tuple
                assert type(pos[0]) is int and type(pos[1]) is int
                assert 0 <= pos[0] < width and 0 <= pos[0] < height

        except:
            self.errorMessage = "Incorrect Target Locations"
            return

        try:
            knownHazardsList = ast.literal_eval(inputs[3])
            assert type(knownHazardsList) is tuple or type(knownHazardsList) is list
            for pos in knownHazardsList:
                assert type(pos) is tuple
                assert type(pos[0]) is int and type(pos[1]) is int
                assert 0 <= pos[0] < width and 0 <= pos[0] < height

        except:
            self.errorMessage = "Incorrect Hazard Locations"
            return

        EasyPygame.nextScene("Scene1", "Scene2")
        EasyPygame.nextSceneOnInit("Scene2", "setInputData", ((width, height, startPos, targetPosList, knownHazardsList), ))

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()