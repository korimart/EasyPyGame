import EasyPygame
from EasyPygame.Components import *

class SkinChanger:
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
