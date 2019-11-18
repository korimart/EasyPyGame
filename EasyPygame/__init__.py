from abc import ABC, abstractmethod
import os.path

import pygame

import EasyPygame.ResourceManager
import EasyPygame.Window
import EasyPygame.Input
import EasyPygame.SceneManager
import EasyPygame.Components

class IApp(ABC):
    @abstractmethod
    def update(self, ms):
        pass

    @abstractmethod
    def render(self, ms):
        pass

def initWindow(width, height, caption, FPS):
    global window
    window = Window.Window(width, height, caption, FPS)

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
    # type: Window.Window
    global window
    rt = rect.copy()
    rt.center = (rect.x, rect.y)
    pygame.draw.rect(window.displaySurface, color, rt)

def _getImageSurf(imageName):
    global resManager, window
    surf = resManager.getLoaded(imageName)
    if not surf:
        raise Exception("File not loaded")

    return surf

def drawImage(imageName, screenRect, imageRect=None, halign="center"):
    surf = _getImageSurf(imageName)
    if not imageRect:
        imageRect = surf.get_rect()

    y = screenRect.y - imageRect.height / 2
    if halign == "left":
        x = screenRect.x - screenRect.width / 2
    elif halign == "right":
        x = screenRect.x + screenRect.width / 2 - imageRect.width
    else:
        x = screenRect.x - imageRect.width / 2

    window.displaySurface.blit(surf, (x, y), imageRect)

def drawStretchedImage(imageName, screenRect, imageRect=None):
    surf = _getImageSurf(imageName)
    if not imageRect:
        imageRect = surf.get_rect()

    surf = pygame.transform.scale(surf, (screenRect.width, screenRect.height))
    rt = screenRect.copy()
    rt.center = (screenRect.x, screenRect.y)
    window.displaySurface.blit(surf, (rt.x, rt.y), imageRect)

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
    surf = DEFAULT_FONT_OBJ.render(text, True, color)
    if center:
        x -= surf.get_width() / 2
        y -= surf.get_height() / 2
    window.displaySurface.blit(surf, (x, y))

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

def nextSceneOnLoad(sceneName, funcName, argTuple):
    global sceneManager
    sceneManager.loadSceneOnLoad(sceneName, funcName, argTuple)

def isMouseOnObject(gameObject):
    screenRect = gameObject.rect.copy()
    screenRect.x, screenRect.y = gameObject.scene.camera.view((screenRect.x, screenRect.y))
    screenRect.x -= screenRect.width / 2
    screenRect.y -= screenRect.height / 2
    mouseX, mouseY = getMousePos()
    return screenRect.collidepoint(mouseX, mouseY)

pygame.init()

window = None # initialized in initWindow()
resManager = ResourceManager.ResourceManager()
inputManager = Input.Input()
sceneManager = SceneManager.SceneManager()

DEFAULT_FONT = "comicsansms"
DEFAULT_FONT_SIZE = 30
loadFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
DEFAULT_FONT_OBJ = pygame.font.SysFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)