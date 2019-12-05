import os, sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(THISDIR))
os.chdir(THISDIR)

import EasyPygame
from EasyPygame.Components import *
from SimApp.Scene1 import Scene1
from SimApp.Scene2 import Scene2

if __name__ == "__main__":
    EasyPygame.initWindow(500, 500, "Robot", 75)
    EasyPygame.loadScene("Scene1")
    EasyPygame.switchScene("Scene1")
    EasyPygame.run()