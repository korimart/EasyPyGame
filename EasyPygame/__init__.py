from abc import ABC, abstractmethod
import os.path

import pygame

import EasyPygame.ResourceManager
import EasyPygame.Window
import EasyPygame.Input
import EasyPygame.SceneManager
import EasyPygame.Renderer
import EasyPygame.Components

class IApp(ABC):
    @abstractmethod
    def update(self, ms):
        pass

    @abstractmethod
    def render(self, ms):
        pass

class EasyPygameRect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.z = 0
        self.width = width
        self.height = height

    def copy(self):
        return EasyPygameRect(self.x, self.y, self.width, self.height)

    def collidepoint(self, x, y):
       return 0 <= x - self.x + self.width / 2 <= self.width \
           and 0 <= y - self.y + self.height / 2 <= self.height

def initWindow(width, height, caption, FPS):
    global window, renderer, resManager
    window = Window.Window(width, height, caption, FPS)
    renderer = Renderer.RendererOpenGL(window, resManager)

def getWindowWidth():
    global window
    return window.width

def getWindowHeight():
    global window
    return window.height

def run():
    global window, inputManager, sceneManager, renderer
    window.run(inputManager, sceneManager, renderer)

def load(fileName):
    global resManager
    return resManager.load(fileName)

def unload(fileName):
    global resManager
    resManager.unload(fileName)

def Rect(x, y, width, height):
    return EasyPygameRect(x, y, width, height)

def drawRect(color, rect):
    global renderer
    renderer.drawRect(color, rect)

def drawImage(imageName, screenRect, imageRect=None, halign="center"):
    global renderer
    renderer.drawImage(imageName, screenRect, imageRect, halign)

def drawStretchedImage(imageName, screenRect, imageRect=None):
    global renderer
    renderer.drawStretchedImage(imageName, screenRect, imageRect)

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

def pprint(text, x, y, center=False, color=(0, 0, 0)):
    global renderer
    renderer.pprint(text, x, y, center, color)

def getScene(sceneName):
    global sceneManager
    return sceneManager.getScene(sceneName)

def switchScene(sceneName):
    global sceneManager
    sceneManager.switchScene(sceneName)

def loadScene(sceneName):
    global sceneManager
    sceneManager.loadScene(sceneName)

def unloadScene(sceneName):
    global sceneManager
    sceneManager.unloadScene(sceneName)

def nextScene(fromSceneName, toSceneName):
    loadScene(toSceneName)
    switchScene(toSceneName)
    unloadScene(fromSceneName)

def nextSceneOnInit(sceneName, funcName, argTuple):
    global sceneManager
    sceneManager.loadSceneOnInit(sceneName, funcName, argTuple)

pygame.init()

window = None # initialized in initWindow()
renderer = None
resManager = ResourceManager.ResourceManager()
inputManager = Input.Input()
sceneManager = SceneManager.SceneManager()