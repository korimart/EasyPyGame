import pygame

class Input:
    def __init__(self):
        self.lastInputList = []
        self.thisInputList = []
        self.thisInputEnabled = dict()

    def isDown(self, inp: str):
        asci = ord(inp.lower())
        return asci in self.thisInputList and self.thisInputEnabled[asci]

    def isDown1stTime(self, inp):
        asci = ord(inp.lower())
        return asci in self.thisInputList and asci not in self.lastInputList and self.thisInputEnabled[asci]

    def consume(self, inp):
        try:
            self.thisInputEnabled[inp] = False
        except:
            pass

    def register(self, inp):
        if inp not in self.thisInputList:
            self.thisInputList.append(inp)

    def unregister(self, inp):
        try:
            self.thisInputList.remove(inp)
        except:
            pass

    def enableInput(self):
        self.thisInputEnabled = {inp : True for inp in self.thisInputList}

    def tick(self):
        self.lastInputList = self.thisInputList[:]