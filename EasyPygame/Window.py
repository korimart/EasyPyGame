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
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)
        self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL)
        pygame.display.set_caption(self.caption)

    def run(self, inputManager, sceneManager, renderer):
        fpsClock = pygame.time.Clock()
        while True:
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
            sceneManager.update()
            sceneManager.currentScene.update(ms)
            sceneManager.currentScene.preRender(ms)
            renderer.clear()
            sceneManager.currentScene.render(ms)
            renderer.render(sceneManager.currentScene.camera)
            sceneManager.currentScene.postRender(ms)
            pygame.display.flip()
            inputManager.tick()
            fpsClock.tick(self.FPS)
