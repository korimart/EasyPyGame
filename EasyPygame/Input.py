import pygame

class Input:
    def __init__(self):
        self.lastInputList = []
        self.thisInputList = []
        self.mousePos = None

    def isDown(self, inp: str):
        return ord(inp.lower()) in self.thisInputList

    def isDown1stTime(self, inp):
        asci = ord(inp.lower())
        return asci in self.thisInputList and asci not in self.lastInputList

    def consume(self, inp):
        pass

    def getMousePos(self):
        pass