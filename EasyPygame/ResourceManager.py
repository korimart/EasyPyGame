import os.path
import json
import pygame

class ResourceManager:
    def __init__(self):
        self.resourceDict = dict()
        self.supportedImageList = [".jpg", ".png", ".bmp"]
        self.fontNameDict = dict()
        self.DEFAULT_FONT = "comicsansms"
        self.DEFAULT_FONT_SIZE = 30
        self.loadFont(self.DEFAULT_FONT, self.DEFAULT_FONT_SIZE)

    def load(self, fileName, override=False):
        _, extension = os.path.splitext(fileName)
        data = None

        if not override and fileName in self.resourceDict:
            return True

        if extension.lower() in self.supportedImageList:
            data = pygame.image.load(fileName)

        if extension.lower() == ".json":
            with open(fileName, "r") as f:
                data = json.load(f)

        if not data:
            raise Exception("resource cannot be loaded; format not supported")
        else:
            self.resourceDict[fileName] = data
            return True

    def unload(self, fileName):
        try:
            del self.resourceDict[fileName]
        except:
            pass

    def getLoaded(self, fileName):
        if fileName in self.resourceDict:
            return self.resourceDict[fileName]
        else:
            raise Exception("File not loaded")
    
    def loadFont(self, fontName, size):
        fontName = "".join(fontName.split())
        try:
            return bool(self.fontNameDict[fontName][size])
        except:
            pass

        font = pygame.font.SysFont(fontName, size)
        if fontName not in self.fontNameDict:
            self.fontNameDict[fontName] = dict()

        self.fontNameDict[fontName][size] = font

    def unloadFont(self, fontName, size):
        fontName = "".join(fontName.split())
        try:
            del self.fontNameDict[fontName][size]
        except:
            pass

    def createTextSurface(self, fontName, size, color, surfaceName, text, override=False):
        fontName = "".join(fontName.split())
        if not override and surfaceName in self.resourceDict:
            raise Exception("imageName already exists")

        try:
            font = self.fontNameDict[fontName][size]
        except:
            raise Exception("font not loaded")

        surf = font.render(text, True, color)
        self.resourceDict[surfaceName] = surf

        