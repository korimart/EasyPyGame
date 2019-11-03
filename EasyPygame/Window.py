import sys
import pygame

class Window:
    def __init__(self, width, height, caption, FPS=200):
        # window
        self.FPS = FPS
        self.width = width
        self.height = height
        self.caption = caption
        self.displaySurface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption(self.caption)

    def run(self, app):
        fpsClock = pygame.time.Clock()
        while True:
            self.displaySurface.fill((255, 255, 255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            ms = fpsClock.get_time()

            app.update(ms)
            app.render(ms)
            pygame.display.update()

            fpsClock.tick(self.FPS)
