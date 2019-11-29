from EasyPygame.Components import *

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.covered = []
        self.uncovered = []
        self.width = width
        self.height = height