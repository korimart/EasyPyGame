import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.uncovered = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.wall = GameObject(scene, "Wall")
        self.wall.uncoveredRects = []
        imageRect = EasyPygame.Rect(32 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.wall.addTextureView(InstancedTextureView("animated.png", self.wall.uncoveredRects, imageRect))
        self.wall.useTextureView(1)

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.tileRects = []
        imageRect = EasyPygame.Rect(128 / 512 + 16 / 512, 16 / 512, 16 / 512, 16 / 512)
        self.colorTiles.addTextureView(InstancedTextureView("animated.png", self.colorTiles.tileRects, imageRect))
        self.colorTiles.useTextureView(1)

    def randomize(self, startingPos, targetList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList)
        self.uncovered = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def getHazardList(self):
        hazardList = []
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j]:
                    hazardList.append((j, i))

        return hazardList

    def restart(self, map):
        pass

    def senseBlob(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            ret = self.terrain[y][x]
            if ret == Terrain.BLOB:
                self.uncovered[y][x] = Terrain.BLOB
                self.uncover(x, y)
                return True
        return False

    def senseHazard(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            ret = self.terrain[y][x]
            if ret == Terrain.HAZARD:
                self.uncovered[y][x] = Terrain.HAZARD
                self.uncover(x, y)
                return True
            return False
        return True

    def uncover(self, x, y):
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        self.wall.uncoveredRects.append(rt)

    def colorTile(self, x, y):
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        self.colorTiles.tileRects.append(rt)

    def clearColor(self):
        del self.colorTiles.tileRects[:]
