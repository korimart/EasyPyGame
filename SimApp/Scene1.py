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
        self.texts = []
        self.submitButton = None
        self.errorMessage = ""
        self.errorMessageTime = 0

    def onLoad(self):
        EasyPygame.load("animated.png")
        data = ["100x100", "(0,0)", "[(99,99), (99, 0)]", "[(1,1)]", "[(3,3)]"]
        for i in range(5):
            inputField = GUI.TextBox(self, ratio=4, name="input" + str(i), defaultText=data[i])
            inputField.transform.translate(-1.5, 2.3 - i * 1.2, 0)
            inputField.transform.scale(0.5, 0.5)
            self.inputFields.append(inputField)

            text = GUI.Text(self, font="monogram.ttf", size=72, color=(1, 1, 1), fixOnCamera=False)
            text.transform.setParent(self.inputFields[i].transform)
            text.transform.translate(-2, 1, 0)
            text.transform.scale(0.7, 0.7)
            self.texts.append(text)

        self.texts[0].setText("Map width X height")
        self.texts[1].setText("Starting Point")
        self.texts[2].setText("List of Target Points")
        self.texts[3].setText("List of Known Hazards")
        self.texts[4].setText("List of Known Blobs")

        self.submitButton = GUI.Button(self, name="Submit", callback=lambda: self.checkInput())
        self.submitButton.transform.translate(2, -2, 0)

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
                assert 0 <= pos[0] < width and 0 <= pos[1] < height

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

        try:
            knownBlobsList = ast.literal_eval(inputs[4])
            assert type(knownBlobsList) is tuple or type(knownBlobsList) is list
            for pos in knownBlobsList:
                assert type(pos) is tuple
                assert type(pos[0]) is int and type(pos[1]) is int
                assert 0 <= pos[0] < width and 0 <= pos[0] < height

        except:
            self.errorMessage = "Incorrect Blob Locations"
            return

        EasyPygame.nextScene("Scene1", "Scene2")
        EasyPygame.nextSceneOnInit("Scene2", "setInputData", ((width, height, startPos, targetPosList, knownHazardsList, knownBlobsList), ))

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()