import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

FLOORTILEZ = -0.03
HAZARDZ = -0.02
COLORTILEZ = -0.01
PATHTAKENZ = -0.005
BLOBZ = 0.01

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.colorTileSpeed = 0.1
        self.colorTileTimer = 0
        self.colorTileBuffer = []

        self.blackSheepWallEnabled = False

        self.hazards = []
        self.blobs = []
        self.uncoveredHazards = []
        self.uncoveredBlobs = []

        self.hazard = GameObject(scene, "Hazard")
        self.blob = GameObject(scene, "Blob")

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.tileRects = []
        self.colorTiles.addTextureView(DefaultInstancedTextureView(self.colorTiles.tileRects, (0, 1, 1), False))
        self.colorTiles.useTextureView(1)

        self.pathTaken = GameObject(scene, "PathTaken")
        self.pathTaken.pathRects = []
        self.pathTaken.addTextureView(DefaultInstancedTextureView(self.pathTaken.pathRects, (0.8, 0.8, 0), False))
        self.pathTaken.useTextureView(1)

    def randomize(self, startingPos, targetList, hazardList, blobList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList, hazardList, blobList)
        self.hazards = []
        self.blobs = []
        self._initHazardBlobList()
        self.blackSheepWall()

        for hazard in hazardList:
            self.uncoveredHazards.append(EasyPygame.EasyPygameRect(*hazard, 1, 1, z=HAZARDZ))

        for blob in blobList:
            self.uncoveredBlobs.append(EasyPygame.EasyPygameRect(*blob, 1, 1, z=BLOBZ))

    def _initHazardBlobList(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j] == Terrain.HAZARD:
                    rect = EasyPygame.EasyPygameRect(j, i, 1, 1, z=HAZARDZ)
                    self.hazards.append(rect)
                elif self.terrain[i][j] == Terrain.BLOB:
                    rect = EasyPygame.EasyPygameRect(j, i, 1, 1, z=BLOBZ)
                    self.blobs.append(rect)

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
        if terrain == Terrain.HAZARD:
            self.uncoveredHazards.append(EasyPygame.EasyPygameRect(x, y, 1, 1, z=HAZARDZ))
        elif terrain == Terrain.BLOB:
            self.uncoveredBlobs.append(EasyPygame.EasyPygameRect(x, y, 1, 1, z=BLOBZ))

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

    def blackSheepWall(self):
        if self.blackSheepWallEnabled:
            rectList = self.hazards
            rectList2 = self.blobs
        else:
            rectList = self.uncoveredHazards
            rectList2 = self.uncoveredBlobs
        
        self.hazard.clearTextureViews()
        imageRect = EasyPygame.Rect(16 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.hazard.addTextureView(InstancedTextureView("animated.png", rectList, imageRect))
        self.hazard.useTextureView(1)

        self.blob.clearTextureViews()
        for i in range(4):
            imageRect = EasyPygame.Rect(288 / 512 + i * 16 / 512, 224 / 512, 16 / 512, 16 / 512)
            self.blob.addTextureView(InstancedTextureView("animated.png", rectList2, imageRect.copy()))
        self.blob.FSM.attachConcurrentState(0, SpriteAnimState(500, [1, 2, 3, 4]))

        self.blackSheepWallEnabled = not self.blackSheepWallEnabled

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
        
        if EasyPygame.isDown1stTime("b"):
            self.blackSheepWall()

        if EasyPygame.isDown1stTime(","):
            if self.colorTileSpeed - 0.1 > 0:
                self.colorTileSpeed -= 0.1
        elif EasyPygame.isDown1stTime("."):
            self.colorTileSpeed += 0.1
