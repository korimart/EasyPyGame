class GameObject:
    def __init__(self, inputHandler, renderer):
        self.screenRect = None
        self.inputHandler = inputHandler
        self.renderer = renderer

    def update(self, ms):
        self.inputHandler.update(self)

    def render(self, ms):
        self.renderer.update(self)