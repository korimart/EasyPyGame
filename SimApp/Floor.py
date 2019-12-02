import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

FLOORTILEZ = -0.03
HAZARDZ = -0.02
COLORTILEZ = -0.01
PATHTAKENZ = -0.005

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.uncovered = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.colorTileSpeed = 0.1
        self.colorTileTimer = 0
        self.colorTileBuffer = []

        self.floorTiles = GameObject(scene, "FloorTile")
        self.floorTiles.addTextureView(TileTextureView("animated.png", \
            EasyPygame.Rect(16 / 512, 64 / 512, 16 / 512, 16 / 512)))
        self.floorTiles.setZ(FLOORTILEZ)
        self.floorTiles.useTextureView(1)

        self.hazard = GameObject(scene, "Hazard")
        self.hazard.rectList = []
        imageRect = EasyPygame.Rect(32 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.hazard.addTextureView(InstancedTextureView("animated.png", self.hazard.rectList, imageRect))
        self.hazard.useTextureView(1)

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.tileRects = []
        self.colorTiles.addTextureView(DefaultInstancedTextureView(self.colorTiles.tileRects, (0, 1, 1)))
        self.colorTiles.useTextureView(1)

        self.pathTaken = GameObject(scene, "PathTaken")
        self.pathTaken.pathRects = []
        self.pathTaken.addTextureView(DefaultInstancedTextureView(self.pathTaken.pathRects, (0.8, 0.8, 0)))
        self.pathTaken.useTextureView(1)

    def randomize(self, startingPos, targetList, hazardList):
        del self.hazard.rectList[:]
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList, hazardList)
        self._prepareHazards()

        for hazard in hazardList:
            self.uncovered.append((Terrain.HAZARD, hazard[0], hazard[1]))

    def _prepareHazards(self):
        rect = EasyPygame.Rect(0, 0, 1, 1)
        rect.z = HAZARDZ
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j]:
                    rect.x, rect.y = j, i
                    self.hazard.rectList.append(rect.copy())

    def restart(self, map):
        pass

    def senseBlob(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            ret = self.terrain[y][x]
            if ret == Terrain.BLOB:
                self.uncover(Terrain.BLOB, x, y)
                return True
        return False

    def senseHazard(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            ret = self.terrain[y][x]
            if ret == Terrain.HAZARD:
                self.uncover(Terrain.HAZARD, x, y)
                return True
            return False
        return True

    def uncover(self, terrain, x, y):
        self.uncovered.append((terrain, x, y))

    def pathed(self, x, y):
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        rt.z = PATHTAKENZ
        self.pathTaken.pathRects.append(rt)

    def colorTile(self, x, y):
        rt = EasyPygame.EasyPygameRect(x, y, 1, 1)
        rt.z = COLORTILEZ
        self.colorTileBuffer.append(rt)

    def clearColor(self):
        self.colorTileBuffer.append(None)

    def yourLogic(self, ms):
        if self.colorTileBuffer:
            self.colorTileTimer += ms
            num = self.colorTileSpeed * self.colorTileTimer
            for _ in range(int(num)):
                try:
                    pop = self.colorTileBuffer.pop(0)
                except:
                    break
                if not pop:
                    del self.colorTiles.tileRects[:]
                else:
                    self.colorTiles.tileRects.append(pop)

            self.colorTileTimer = 0
