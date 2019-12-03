import EasyPygame
from EasyPygame.Components import *

# class DefaultSkinChanger:
#     def changeRobot(self, robot):
#         robot.clearTextureViews()
#         robot.addTextureView(DefaultTextureView()) # idle left
#         robot.addTextureView(DefaultTextureView((0.4, 0.4, 1))) # idle right
#         robot.addTextureView(DefaultTextureView((1, 0, 0))) # work left
#         robot.addTextureView(DefaultTextureView((1, 0.4, 0.4))) # work right

#         func = lambda a: a < 2

#         idle = TerneryState("facing", func, StaticTextureState(1), StaticTextureState(2))
#         work = TerneryState("facing", func, StaticTextureState(3), StaticTextureState(4))

#         robot.FSM.clearConcurrentStates()
#         robot.FSM.attachConcurrentState(robot.idle, idle)
#         robot.FSM.attachConcurrentState(robot.running, work)
#         robot.FSM.attachConcurrentState(robot.working, work)
#         robot.FSM.switchState(robot.idle, 0)

class DungeonSkinChanger:
    def changeRobot(self, robot):
        for i in range(4):
            compList = []
            imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * i, 16 / 512, 16 / 512, 16 / 512)
            compList.append(TextureRenderComponent("animated.png", imageRect.copy(), flipX=True, blending=True))

        robot.idleRC = AnimationRenderComponent(compList, 500)

        for i in range(4):
            compList = []
            imageRect = EasyPygame.Rect(128 / 512 + 16 / 512 * (i + 4), 16 / 512, 16 / 512, 16 / 512)
            compList.append(TextureRenderComponent("animated.png", imageRect.copy(), flipX=True, blending=True))

        robot.runningRC = AnimationRenderComponent(compList, 500)

        robot.arrow.renderComp = DefaultRenderComponent((0.5, 0.5, 0))