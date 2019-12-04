import glm
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

        self.colorTileSpeed = 0.01 # tile per ms
        self.colorTileTimer = 0
        self.colorTileBuffer = []

        self.blackSheepWallEnabled = False

        self.hazard = GameObject(scene, "Hazard")
        self.allHazardsRC = None
        self.knownHazardsRC = None

        self.blob = GameObject(scene, "Blob")
        self.allBlobsRC = None
        self.knownBlobsRC = None

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.renderComp = DefaultInstancedRenderComponent(None, (0, 1, 1), False, size=width*height, static=False)
        self.pathTaken = GameObject(scene, "PathTaken")
        self.pathTaken.renderComp = DefaultInstancedRenderComponent(None, (0.8, 0.8, 0), False, size=width*height, static=False)

        # self.hazards = []
        # self.blobs = []
        # self.uncoveredHazards = []
        # self.uncoveredBlobs = []

        # self.hazard = GameObject(scene, "Hazard")
        # self.blob = GameObject(scene, "Blob")

        # self.colorTiles = GameObject(scene, "ColorTile")
        # self.colorTiles.tileRects = []
        # self.colorTiles.addTextureView(DefaultInstancedTextureView(self.colorTiles.tileRects, (0, 1, 1), False))
        # self.colorTiles.useTextureView(1)

        # self.pathTaken = GameObject(scene, "PathTaken")
        # self.pathTaken.pathRects = []
        # self.pathTaken.addTextureView(DefaultInstancedTextureView(self.pathTaken.pathRects, (0.8, 0.8, 0), False))
        # self.pathTaken.useTextureView(1)

    def randomize(self, startingPos, targetList, hazardList, blobList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList, hazardList, blobList)
        self._initHazardBlob()
        self.blackSheepWall()

        for hazard in hazardList:
            self.uncover(Terrain.HAZARD, *hazard)

        for blob in blobList:
            self.uncover(Terrain.BLOB, *blob)

    def _initHazardBlob(self):
        hazards = []
        blobs = []
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j] == Terrain.HAZARD:
                    hazards.append(glm.translate(glm.mat4(), glm.vec3(j, i, HAZARDZ)))
                elif self.terrain[i][j] == Terrain.BLOB:
                    blobs.append(glm.translate(glm.mat4(), glm.vec3(j, i, BLOBZ)))

        self.allHazardsRC = DefaultInstancedRenderComponent(hazards)
        self.allBlobsRC = DefaultInstancedRenderComponent(blobs, (1, 0, 0))
        self.knownHazardsRC = DefaultInstancedRenderComponent(None, size=len(hazards), static=False)
        self.knownBlobsRC = DefaultInstancedRenderComponent(None, size=len(blobs), static=False)

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
            self.knownHazardsRC.append(glm.translate(glm.mat4(), glm.vec3(x, y, HAZARDZ)))
        elif terrain == Terrain.BLOB:
            self.knownBlobsRC.append(glm.translate(glm.mat4(), glm.vec3(x, y, BLOBZ)))

    def pathed(self, x, y):
        self.pathTaken.renderComp.append(glm.translate(glm.mat4(), glm.vec3(x, y, PATHTAKENZ)))

    def colorTile(self, x, y):
        self.colorTileBuffer.append((x, y))

    def clearColor(self):
        self.colorTileBuffer.append(None)

    def blackSheepWall(self):
        if self.blackSheepWallEnabled:
            self.hazard.renderComp = self.allHazardsRC
            self.blob.renderComp = self.allBlobsRC
        else:
            self.hazard.renderComp = self.knownHazardsRC
            self.blob.renderComp = self.knownBlobsRC

        # self.hazard.clearTextureViews()
        # imageRect = EasyPygame.Rect(16 / 512, 12 / 512, 16 / 512, 16 / 512)
        # self.hazard.addTextureView(InstancedTextureView("animated.png", rectList, imageRect))
        # self.hazard.useTextureView(1)

        # self.blob.clearTextureViews()
        # for i in range(4):
        #     imageRect = EasyPygame.Rect(288 / 512 + i * 16 / 512, 224 / 512, 16 / 512, 16 / 512)
        #     self.blob.addTextureView(InstancedTextureView("animated.png", rectList2, imageRect.copy()))
        # self.blob.FSM.attachConcurrentState(0, SpriteAnimState(500, [1, 2, 3, 4]))

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
                    self.colorTiles.renderComp.clear()
                else:
                    self.colorTiles.renderComp.append(glm.translate(glm.mat4(), glm.vec3(*pop, COLORTILEZ)))

            self.colorTileTimer = 0

        if EasyPygame.isDown1stTime("b"):
            self.blackSheepWall()

        if EasyPygame.isDown1stTime(","):
            if self.colorTileSpeed - 0.1 > 0:
                self.colorTileSpeed -= 0.1
        elif EasyPygame.isDown1stTime("."):
            self.colorTileSpeed += 0.1
