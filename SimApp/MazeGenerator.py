from random import randint

class Terrain:
    NOTHING = 0
    HAZARD = 1
    BLOB = 2

class MazeGenerator:
    DIRECTIONS = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    DIRECTIONS1 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def generate(self, width, height, startingPos, targetList):
        # from world space to array space (flip x y)
        targets = [(startingPos[1], startingPos[0])]
        for target in targetList:
            targets.append((target[1], target[0]))
        stack = []
        start = targets[0]
        xEven = start[0] % 2
        yEven = start[1] % 2
        # cells surrounded by 4 walls
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

        return ret

# # for _ in range(100):
# #     targetList = []
# #     for _ in range(10):
# #         a = randint(0, 99)
# #         b = randint(0, 99)
# #         targetList.append((a, b))
# #     maze = MazeGenerator().generate(100, 100, targetList)

# #     for target in targetList:
# #         if maze[target[0]][target[1]] == Terrain.HAZARD:
# #             raise Exception("lul")

# maze = MazeGenerator().generate(10, 10, [(0, 0), (0, 3), (1, 4)])
# print(maze)