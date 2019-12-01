import EasyPygame
from EasyPygame.Components import *

class DefaultSkinChanger:
    def changeRobot(self, robot):
        robot.clearTextureViews()
        robot.addTextureView(DefaultTextureView()) # idle left
        robot.addTextureView(DefaultTextureView((0.4, 0.4, 1))) # idle right
        robot.addTextureView(DefaultTextureView((1, 0, 0))) # work left
        robot.addTextureView(DefaultTextureView((1, 0.4, 0.4))) # work right

        func = lambda a: a < 2

        idle = TerneryState("facing", func, StaticTextureState(1), StaticTextureState(2))
        work = TerneryState("facing", func, StaticTextureState(3), StaticTextureState(4))

        robot.FSM.clearConcurrentStates()
        robot.FSM.attachConcurrentState(robot.idle, idle)
        robot.FSM.attachConcurrentState(robot.running, work)
        robot.FSM.attachConcurrentState(robot.working, work)
        robot.FSM.switchState(robot.idle, 0)

class DungeonSkinChanger:
    def changeRobot(self, robot):
        robot.clearTextureViews()
        robot.FSM.clearConcurrentStates()

        for i in range(4):
            imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * i, 16 / 512, 16 / 512, 16 / 512)
            robot.addTextureView(TextureView("animated.png", imageRect.copy(), flipX=True))
            robot.addTextureView(TextureView("animated.png", imageRect))

        for i in range(4):
            imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * (i + 4), 16 / 512, 16 / 512, 16 / 512)
            robot.addTextureView(TextureView("animated.png", imageRect.copy(), flipX=True))
            robot.addTextureView(TextureView("animated.png", imageRect))

        func = lambda a: a >= 2

        idle = TerneryState("lastFace", func, SpriteAnimState(500, [1, 3, 5, 7]), SpriteAnimState(500, [2, 4, 6, 8]))
        run = TerneryState("lastFace", func, SpriteAnimState(250, [9, 11, 13, 15]), SpriteAnimState(250, [10, 12, 14, 16]))

        robot.FSM.attachConcurrentState(robot.idle, idle)
        robot.FSM.attachConcurrentState(robot.running, run)
        robot.FSM.attachConcurrentState(robot.working, idle)
        robot.FSM.switchState(robot.idle, 0)