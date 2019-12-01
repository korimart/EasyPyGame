import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

count = 0

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.uncovered = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.colorTileSpeed = 1000000000
        self.colorTileTimer = 0
        self.colorTileBuffer = []

        self.hazard = GameObject(scene, "Hazard")
        self.hazard.uncoveredRects = []
        imageRect = EasyPygame.Rect(32 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.hazard.addTextureView(InstancedTextureView("animated.png", self.hazard.uncoveredRects, imageRect))
        self.hazard.useTextureView(1)

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.tileRects = []
        self.colorTiles.addTextureView(DefaultInstancedTextureView(self.colorTiles.tileRects, (0, 1, 1)))
        self.colorTiles.useTextureView(1)

    def randomize(self, startingPos, targetList, hazardList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList, hazardList)
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
        rt.z = -0.002
        self.hazard.uncoveredRects.append(rt)

    # def colorTile(self, x, y):
    #     rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
    #     rt.z = -0.001
    #     self.colorTileBuffer.append(rt)

    def colorTile(self, x, y):
        global count
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        rt.z = -0.001
        self.colorTiles.tileRects.append(rt)
        # count += 1
        # print(count)

    def clearColor(self):
        del self.colorTiles.tileRects[:]

    # def yourLogic(self, ms):
    #     global count
    #     if self.colorTileBuffer:
    #         self.colorTileTimer += ms
    #         if self.colorTileTimer > 1 / self.colorTileSpeed:
    #             count += 1
    #             print(count)
    #             pop = self.colorTileBuffer.pop(0)
    #             self.colorTiles.tileRects.append(pop)
    #             self.colorTileTimer = 0

