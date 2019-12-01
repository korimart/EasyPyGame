class Map:
    def __init__(self, size, hazards, searchPoints, robotLocation, minPoints=(0,0)):
        self.hazards = self.initHazards(hazards)
        self.searchPoints = set(searchPoints)
        self.visitedSearchPoints = set()
        self.unvisitedSearchPoints = set(searchPoints)
        self.blobs = set()
        self.robotLocation = robotLocation
        self.size = size
        self.pathTaken = []
        self.pathToBeTaken = []
        self.minPoints = minPoints

    def initHazards(self, points):
        d = {}
        for p in points:
            d[p] = 1
        return d

    #should be deleted
    def initList(self, size, points):
        x = size[0]
        y = size[1]
        l = [ [0] * y for i in range(x)]
        for p in points:
            l[p[0]][p[1]] = 1

    def update(self, robotLocation, hazards=[], blobs=[]):
        for h in hazards:
            self.hazards[h] = 1
        for b in blobs:
            if b in self.blobs:
                pass
            else:
                self.blobs.add(b)
        self.robotLocation = robotLocation
        if robotLocation in self.searchPoints:
            self.visitedSearchPoints.add(robotLocation)
            if robotLocation in self.unvisitedSearchPoints:
                self.unvisitedSearchPoints.remove(robotLocation)

    def isOnPath(self):
        for p in self.pathToBeTaken:
            if p in self.hazards:
                return True
            else:
                return False

    def nextDestination(self):
        return self.pathToBeTaken.pop(0)

    def currentPos(self):
        return self.robotLocation

    def getVisitedSearchPoints(self):
        return self.visitedSearchPoints

    def setVisitedSearchPoints(self, location):
        self.visitedSearchPoints.add(location)

    def getUnvisitedSearchPoints(self):
        return self.unvisitedSearchPoints.copy()

    def getTerrain(self, x, y):
        pos = (x, y)
        if pos in self.hazards:
            return 1
        if pos[0] < self.minPoints[0]:
            return 1
        if pos[1] < self.minPoints[1]:
            return 1
        if pos[0] >= self.size[0]:
            return 1
        if pos[1] >= self.size[1]:
            return 1
        return 0