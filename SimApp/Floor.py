import glm
import EasyPygame
from EasyPygame.Components import *
from SimApp.MazeGenerator import *

FLOORTILEZ = -0.03
HAZARDZ = -0.02
COLORTILEZ = -0.01
PATHTAKENZ = -0.005
PATHZ = -0.03
BLOBZ = 0.01

class Floor(GameObject):
    def __init__(self, scene, width, height):
        super().__init__(scene, "Floor")
        self.terrain = []
        self.width = width
        self.height = height
        self.mazeGenerator = MazeGenerator()

        self.colorTileSpeed = 0.05 # tile per ms
        self.colorTileTimer = 0
        self.colorTileBuffer = []

        self.pathLength = 0
        self.pathSpeed = 0.001 # path per ms
        self.pathTimer = 0
        self.pathBuffer = []

        self.blackSheepWallEnabled = False

        self.known = []

        self.hazard = GameObject(scene, "Hazard")
        self.allHazardsRC = None
        self.knownHazardsRC = None

        self.blob = GameObject(scene, "Blob")
        self.allBlobsRC = None
        self.knownBlobsRC = None

        self.colorTiles = GameObject(scene, "ColorTile")
        self.colorTiles.renderComp = DefaultInstancedRenderComponent(None, (251/255, 234/255, 235/255), \
            False, size=width*height, static=False)

        self.pathTaken = GameObject(scene, "PathTaken")
        self.pathTaken.renderComp = DefaultInstancedRenderComponent(None, (0.8, 0.8, 0), \
            False, size=width*height, static=False)

        self.pathTiles = GameObject(scene, "Path")
        self.pathTiles.renderComp = DefaultInstancedRenderComponent(None, (236 / 255, 77 / 255, 55 / 255), \
            False, size=width*height, static=False)

        self.target = GameObject(scene, "Target")

    def randomize(self, startingPos, targetList, hazardList, blobList):
        self.terrain = self.mazeGenerator.generate(self.width, self.height, startingPos, targetList, hazardList, blobList)
        self._initRC(targetList)
        self.blackSheepWall()

        for hazard in hazardList:
            self.uncover(Terrain.HAZARD, *hazard)

        for blob in blobList:
            self.uncover(Terrain.BLOB, *blob)

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
        if (x, y) in self.known:
            return

        if terrain == Terrain.HAZARD:
            self.knownHazardsRC.append(glm.translate(glm.mat4(), glm.vec3(x, y, HAZARDZ)))
        elif terrain == Terrain.BLOB:
            self.knownBlobsRC.append(glm.translate(glm.mat4(), glm.vec3(x, y, BLOBZ)))

        self.known.append((x, y))

    def scalePathDrawSpeed(self, scale):
        self.pathSpeed *= scale

    def scaleTileDrawSpeed(self, scale):
        self.colorTileSpeed *= scale

    def pathed(self, x, y):
        self.pathTaken.renderComp.append(glm.translate(glm.mat4(), glm.vec3(x, y, PATHTAKENZ)))

    def colorTile(self, x, y):
        self.colorTileBuffer.append((x, y))

    def colorPath(self, path):
        self.pathLength = len(path)
        self.pathBuffer = path

    def clearColor(self):
        self.colorTileBuffer.append(None)

    def draw(self, ms):
        if self.colorTileBuffer:
            self.colorTileTimer += ms
            num = int(self.colorTileSpeed * self.colorTileTimer)

            if num:
                self.colorTileTimer = 0
                for _ in range(num):
                    try:
                        pop = self.colorTileBuffer.pop(0)
                    except:
                        break
                    if not pop:
                        self.colorTiles.renderComp.clear()
                        self.pathTiles.renderComp.clear()
                    else:
                        self.colorTiles.renderComp.append(glm.translate(glm.mat4(), glm.vec3(*pop, COLORTILEZ)))

        elif self.pathBuffer:
            self.pathTimer += ms
            num = int(self.pathSpeed * self.pathLength * self.pathTimer)

            if num:
                self.pathTimer = 0
                for _ in range(num):
                    try:
                        pop = self.pathBuffer.pop(0)
                    except:
                        break
                    self.pathTiles.renderComp.append(glm.translate(glm.mat4(), glm.vec3(*pop, PATHZ)))

        if not self.colorTileBuffer and not self.pathBuffer:
            return False

        return True

    def blackSheepWall(self):
        if self.blackSheepWallEnabled:
            self.hazard.renderComp = self.allHazardsRC
            self.blob.renderComp = self.allBlobsRC
        else:
            self.hazard.renderComp = self.knownHazardsRC
            self.blob.renderComp = self.knownBlobsRC

        self.blackSheepWallEnabled = not self.blackSheepWallEnabled

    def needToDraw(self):
        return self.colorTileBuffer or self.pathBuffer

    def _initRC(self, targetList):
        hazards = []
        blobs = []
        targets = []
        for i in range(self.height):
            for j in range(self.width):
                if self.terrain[i][j] == Terrain.HAZARD:
                    hazards.append(glm.translate(glm.mat4(), glm.vec3(j, i, HAZARDZ)))
                elif self.terrain[i][j] == Terrain.BLOB:
                    blobs.append(glm.translate(glm.mat4(), glm.vec3(j, i, BLOBZ)))

        for target in targetList:
            mat = glm.translate(glm.mat4(), glm.vec3(target[0], target[1] + 0.7, BLOBZ))
            targets.append(mat)

        imageRectList = []
        for i in range(4):
            imageRectList.append(EasyPygame.Rect(288 / 512 + i * 16 / 512, 224 / 512, 16 / 512, 16 / 512))

        imageRect = EasyPygame.Rect(16 / 512, 12 / 512, 16 / 512, 16 / 512)
        self.allHazardsRC = TextureInstancedRenderComponent(hazards, "animated.png", imageRect=imageRect)

        self.allBlobsRC = AnimationRenderComponent(TextureInstancedRenderComponent(blobs, "animated.png", blending=True),\
            imageRectList, 500)

        self.knownHazardsRC = TextureInstancedRenderComponent(None, "animated.png", imageRect=imageRect, size=len(hazards), static=False)

        self.knownBlobsRC = AnimationRenderComponent(\
            TextureInstancedRenderComponent(None, "animated.png", size=len(blobs), static=False, blending=True),\
                imageRectList, 500)

        imageRectList = []
        for i in range(4):
            imageRectList.append(EasyPygame.Rect(i * 128 / 641, 0, 128 / 641, 1))

        self.target.renderComp = AnimationRenderComponent(TextureInstancedRenderComponent(targets, "arrow.png", blending=True, flipY=True),\
            imageRectList, 500)