import sys
import pygame
from EasyPygame.Input import Input

class Window:
    def __init__(self, width, height, caption, FPS=200):
        # window
        self.FPS = FPS
        self.width = width
        self.height = height
        self.caption = caption
        self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption(self.caption)

    def run(self, inputManager, sceneManager):
        fpsClock = pygame.time.Clock()
        while True:
            self.displaySurface.fill((255, 255, 255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    inputManager.register(event.key)

                elif event.type == pygame.KEYUP:
                    inputManager.unregister(event.key)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    inputManager.register(event.button)

                elif event.type == pygame.MOUSEBUTTONUP:
                    inputManager.unregister(event.button)

            ms = fpsClock.get_time()

            inputManager.enableInput()
            sceneManager.currentScene.update(ms)
            sceneManager.currentScene.preRender()
            sceneManager.currentScene.render(ms)
            sceneManager.currentScene.postRender()
            pygame.display.update()
            inputManager.tick()
            fpsClock.tick(self.FPS)
