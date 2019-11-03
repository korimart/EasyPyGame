from abc import ABC, abstractmethod
import os.path

import pygame

import EasyPygame.ResourceManager
import EasyPygame.Window
import EasyPygame.Input
# import Animator

class IApp(ABC):
    @abstractmethod
    def update(self, ms):
        pass

    @abstractmethod
    def render(self, ms):
        pass

window = None
resManager = None
inputManager = None

def init(width, height, caption, FPS):
    global window, resManager, inputManager
    pygame.init()
    window = Window.Window(width, height, caption, FPS)
    resManager = ResourceManager.ResourceManager()
    inputManager = Input.Input()

def run(app):
    global window, inputManager
    window.run(inputManager, app)

def load(fileName):
    global resManager
    return resManager.load(fileName)

# TODO
def unload(fileName):
    global resManager
    pass

def Rect(x, y, width, height):
    return pygame.Rect(x, y, width, height)

def drawRect(color, rect):
    # type: Window.Window
    global window
    pygame.draw.rect(window.displaySurface, color, rect)

def drawImage(imageName, screenRect, imageRect=None):
    # type: ResourceManager.ResourceManager
    global resManager, window
    surf = resManager.getLoaded(imageName)
    if not surf:
        raise Exception("File not loaded")

    if not imageRect:
        imageRect = surf.get_rect()

    window.displaySurface.blit(surf, (screenRect.x, screenRect.y), imageRect)

def isDown(inp):
    global inputManager
    return inputManager.isDown(inp)

def isDown1stTime(inp):
    global inputManager
    return inputManager.isDown1stTime(inp)

def consume(inp):
    global inputManager
    inputManager.consume(inp)

def getMousePos():
    return pygame.mouse.get_pos()

def loadFont(fontName, size):
    global resManager
    resManager.loadFont(fontName, size)

def createTextImage(fontName, size, color, imageName, text):
    global resManager
    resManager.createTextSurface(fontName, size, color, imageName, text)