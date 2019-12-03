from random import randint, random

class Terrain:
    NOTHING = 0
    HAZARD = 1
    BLOB = 2

class MazeGenerator:
    DIRECTIONS = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    DIRECTIONS1 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def generate(self, width, height, startingPos, targetList, hazardList, blobList):
        # from world space to array space (flip x y)
        targets = [(startingPos[1], startingPos[0])]
        for target in targetList:
            targets.append((target[1], target[0]))
        stack = []
        start = targets[0]
        xEven = start[0] % 2
        yEven = start[1] % 2

        # cells are surrounded by 4 walls
        ret = [[Terrain.NOTHING if i % 2 == xEven else Terrain.HAZARD \
            for i in range(width)] if j % 2 == yEven else \
                [Terrain.HAZARD for _ in range(width)] for j in range(height)]

        visited = [[False for _ in range(width)] for _ in range(height)]
        visited[start[0]][start[1]] = True
        stack.append(start)

        while len(stack) > 0:
            curr = stack.pop()
            neighbors = []
            for delta in self.DIRECTIONS:
                nei = (curr[0] + delta[0], curr[1] + delta[1])
                if 0 <= nei[0] < height and 0 <= nei[1] < width and not visited[nei[0]][nei[1]]:
                    neighbors.append(nei)
            if neighbors:
                stack.append(curr)
                index = randint(0, len(neighbors) - 1)
                chosen = neighbors[index]
                ret[(curr[0] + chosen[0]) // 2][(curr[1] + chosen[1]) // 2] = Terrain.NOTHING
                visited[chosen[0]][chosen[1]] = True
                stack.append(chosen)

        # targets should not be blocked or isolated
        for curr in targets:
            while True:
                ret[curr[0]][curr[1]] = Terrain.NOTHING
                neighbors = []
                for delta in self.DIRECTIONS1:
                    nei = (curr[0] + delta[0], curr[1] + delta[1])
                    if 0 <= nei[0] < height and 0 <= nei[1] < width:
                        neighbors.append(nei)
                        if ret[nei[0]][nei[1]] == Terrain.NOTHING:
                            break
                else: # if not break
                    index = randint(0, len(neighbors) - 1)
                    chosen = neighbors[index]
                    curr = chosen
                    continue
                break

        for i in range(height):
            for j in range(width):
                if ret[i][j] == Terrain.NOTHING:
                    if random() < 0.05:
                        ret[i][j] = Terrain.BLOB
            
        for hazard in hazardList:
            ret[hazard[1]][hazard[0]] = Terrain.HAZARD

        # doesn't care if isolated
        for blob in blobList:
            ret[blob[1]][blob[0]] = Terrain.BLOB

        return ret

class FieldGenerator:
    def generate(self, width, height, startingPos, targetList, hazardList):
        ret = [[0 for _ in range(width)] for _ in range(height)]
        return ret