import os, sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))

import EasyPygame
import ast

class Scene1(EasyPygame.Components.Scene):
    ERRORMESSAGETIME = 2000
    def __init__(self):
        super().__init__()
        self.inputFields = []
        self.submitButton = None
        self.errorMessage = ""
        self.errorMessageTime = 0

    def onLoad(self):
        for i in range(4):
            inputField = EasyPygame.Components.GUI.TextBox(self, "input" + str(i), "Type Here")
            inputField.rect.x = -100
            inputField.rect.y = 200 - 100 * i
            inputField.rect.width = 200
            self.inputFields.append(inputField)

        self.submitButton = EasyPygame.Components.GUI.Button(self, "Submit")
        self.submitButton.rect.x = 150
        self.submitButton.rect.y = -100
        self.submitButton.setCallback(lambda: self.checkInput())

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
            assert type(startPos) is tuple or type(startPos) is list
            assert type(startPos[0]) is int and type(startPos[1]) is int
            assert 0 <= startPos[0] < width and 0 <= startPos[0] < height
        except:
            self.errorMessage = "Incorrect Starting Locations"
            return

        try:
            targetPosList = ast.literal_eval(inputs[2])
            assert type(targetPosList) is tuple or type(targetPosList) is list
            for pos in targetPosList:
                assert type(pos) is tuple or type(pos) is list
                assert type(pos[0]) is int and type(pos[1]) is int
                assert 0 <= pos[0] < width and 0 <= pos[0] < height

        except:
            self.errorMessage = "Incorrect Target Locations"
            return

        try:
            knownHazardsList = ast.literal_eval(inputs[3])
            assert type(knownHazardsList) is tuple or type(knownHazardsList) is list
            for pos in knownHazardsList:
                assert type(pos) is tuple or type(pos) is list
                assert type(pos[0]) is int and type(pos[1]) is int
                assert 0 <= pos[0] < width and 0 <= pos[0] < height

        except:
            self.errorMessage = "Incorrect Hazard Locations"
            return

        EasyPygame.nextScene("Scene1", "Scene2")
        scene2 = EasyPygame.getScene("Scene2")
        scene2.setInputData(width, height, startPos, targetPosList, knownHazardsList)
        

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()