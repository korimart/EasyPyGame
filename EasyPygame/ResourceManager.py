import os.path
import json
import array
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

    def createTextTexture(self, handleName, font, size, text, color):
        # return size
        name = (font + str(size)).lower()
        try:
            fontObj = self.fontDict[name]
        except:
            fontObj = ImageFont.truetype(font, size * 5)
            self.fontDict[name] = fontObj

        ascent, descent = fontObj.getmetrics()
        width, _ = self.draw.textsize(text, font=fontObj)
        height = ascent + descent
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, color, font=fontObj)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        try:
            glDeleteTextures([self.textureDict[handleName]])
        except KeyError:
            pass
        self.textureDict[handleName] = texture
        return (width, height)

    def getTexture(self, fileName):
        if fileName in self.textureDict:
            return self.textureDict[fileName]
        else:
            raise Exception("Texture not loaded: " + fileName)
