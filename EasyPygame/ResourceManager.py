import os.path
import json
import pygame
from OpenGL.GL import *
from PIL import ImageDraw, ImageFont, Image

class ResourceManager:
    def __init__(self):
        self.resourceDict = dict()
        self.textureDict = dict()
        self.supportedImageList = [".jpg", ".png", ".bmp"]
        self.fontDict = dict()

        self.img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)

    def load(self, fileName, override=False):
        _, extension = os.path.splitext(fileName)
        data = None

        if not override and fileName in self.resourceDict:
            return True

        if extension.lower() in self.supportedImageList:
            data = pygame.image.load(fileName)
            textureData = pygame.image.tostring(data, "RGBA")
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, data.get_width(), data.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
            self.textureDict[fileName] = texture

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

    def createTextTexture(self, font, size, text, color):
        # return size
        name = (font + str(size)).lower()
        try:
            fontObj = self.fontDict[name]
        except:
            fontObj = ImageFont.truetype(font, size)
            self.fontDict[name] = fontObj

        width, height = self.draw.textsize(text, font=fontObj)
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, color, font=fontObj)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        self.textureDict[fileName] = texture
        # TODO

    def getLoaded(self, fileName):
        if fileName in self.resourceDict:
            return self.resourceDict[fileName]
        else:
            raise Exception("File not loaded")

    def getTexture(self, fileName):
        if fileName in self.textureDict:
            return self.textureDict[fileName]
        else:
            raise Exception("Texture not loaded: " + fileName)

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

    def createTextSurface(self, fontName, size, color, surfaceName, text, override=False, background=None):
        fontName = "".join(fontName.split())
        if not override and surfaceName in self.resourceDict:
            raise Exception("imageName already exists")

        try:
            font = self.fontNameDict[fontName][size]
        except:
            raise Exception("font not loaded")

        surf = font.render(text, True, color, background)
        self.resourceDict[surfaceName] = surf

