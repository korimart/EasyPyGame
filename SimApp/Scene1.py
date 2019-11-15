import os, sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))

import EasyPygame

class Scene1(EasyPygame.Components.Scene):
    def __init__(self):
        super().__init__()
        self.inputFields = []
        self.submitButton = None

    def onLoad(self):
        for i in range(4):
            inputField = EasyPygame.Components.GUI.TextBox(self, "input" + str(i), "Type Here")
            inputField.rect.x = -100
            inputField.rect.y = 200 - 100 * i
            inputField.rect.width = 200
            self.inputFields.append(inputField)

        self.submitButton = EasyPygame.Components.GUI.Button(self)
        self.submitButton.rect.x = 150
        self.submitButton.rect.y = -100
        self.submitButton.setCallback(lambda: self.checkInput())

    def checkInput(self):
        print("checking input")

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Sample", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()