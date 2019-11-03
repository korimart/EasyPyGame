import os.path
import json
import pygame

class ResourceManager:
    def __init__(self):
        self.resourceDict = dict()
        self.supportedImageList = [".jpg", ".png", ".bmp"]

    def load(self, fileName):
        _, extension = os.path.splitext(fileName)
        data = None

        if fileName in self.resourceDict:
            return True

        if extension.lower() in self.supportedImageList:
            data = pygame.image.load(fileName)

        if extension.lower() == ".json":
            with open(fileName, "r") as f:
                data = json.load(f)

        if not data:
            return False
        else:
            self.resourceDict[fileName] = data
            return True

    def getLoaded(self, fileName):
        if fileName in self.resourceDict:
            return self.resourceDict[fileName]
        else:
            return None
            