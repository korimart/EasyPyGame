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

def initWindow(width, height, caption, FPS):
    global window, renderer, resManager
    window = Window.Window(width, height, caption, FPS)
    renderer = Renderer.Renderer(window.displaySurface, resManager)

def getWindowWidth():
    global window
    return window.width

def getWindowHeight():
    global window
    return window.height

def run():
    global window, inputManager, sceneManager
    window.run(inputManager, sceneManager)

def load(fileName):
    global resManager
    return resManager.load(fileName)

def unload(fileName):
    global resManager
    resManager.unload(fileName)

def Rect(x, y, width, height):
    return pygame.Rect(x, y, width, height)

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

def loadFont(fontName, size):
    global resManager
    resManager.loadFont(fontName, size)

def unloadFont(fontName, size):
    global resManager
    resManager.unloadFont(fontName, size)

def createTextImage(fontName, size, color, imageName, text, override=False):
    global resManager
    resManager.createTextSurface(fontName, size, color, imageName, text, override)

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

def isMouseOnObject(gameObject):
    screenRect = gameObject.rect.copy()
    screenRect.x, screenRect.y = gameObject.scene.camera.view((screenRect.x, screenRect.y))
    screenRect.x -= screenRect.width / 2
    screenRect.y -= screenRect.height / 2
    mouseX, mouseY = getMousePos()
    return screenRect.collidepoint(mouseX, mouseY)

pygame.init()

window = None # initialized in initWindow()
renderer = None
resManager = ResourceManager.ResourceManager()
inputManager = Input.Input()
sceneManager = SceneManager.SceneManager()