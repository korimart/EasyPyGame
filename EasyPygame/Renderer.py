import pygame

class Renderer:
    def __init__(self, displaySurf, resManager):
        self.surface = displaySurf
        self.resManager = resManager

    def renderDefault(self, worldRect, camera, color, name):
        # world
        targetRect = worldRect

        # view
        targetRect.x, targetRect.y = camera.view([worldRect.x, worldRect.y])

        # proj
        self._distanceDivision(camera.distance, targetRect)

        # screen space
        targetRect.x += self.surface.get_width() / 2
        targetRect.y = self.surface.get_height() / 2 - targetRect.y

        self.drawRect(color, targetRect)
        self.pprint(name, targetRect.x, targetRect.y, True, scale=(1 / camera.distance, 1 / camera.distance))

        retRect = targetRect.copy()
        retRect.center = (retRect.x, retRect.y)
        return retRect

    def renderTextured(self, worldRect, camera, textureView):
        imageSurf = self.resManager.getLoaded(textureView.texture)
        if not textureView.imageRect:
            imageRect = imageSurf.get_rect().copy()
        else:
            imageRect = textureView.imageRect.copy()

        # world
        targetRect = worldRect
        scale = list(textureView.scale)

        if not textureView.fitObject and not textureView.crop:
            targetRect.width, targetRect.height = (imageRect.width, imageRect.height)

        targetRect.width  *= scale[0]
        targetRect.height *= scale[1]
        imageRect.width   *= scale[0]
        imageRect.height  *= scale[1]

        # view
        targetRect.x, targetRect.y = camera.view([worldRect.x, worldRect.y])

        # proj
        self._distanceDivision(camera.distance, targetRect)

        # if fitObject, image does not need to be scaled by distance and will be shrinked later
        if not textureView.fitObject:
            imageRect.width   *= 1 / camera.distance
            imageRect.height  *= 1 / camera.distance
            imageSurf = pygame.transform.scale(imageSurf, (imageRect.width, imageRect.height))

        # convert to screen space
        # targetRect is in screen space but with x y being its center
        targetRect.x += self.surface.get_width() / 2
        targetRect.y = self.surface.get_height() / 2 - targetRect.y

        targetRect.x += textureView.relPos[0]
        targetRect.y -= textureView.relPos[1]

        # convert targetRect to image space and get imageRect
        if textureView.crop:
            if textureView.halign == "left":
                left = 0
                right = targetRect.width
            elif textureView.halign == "right":
                right = imageRect.width
                left = right - targetRect.width
            else:
                left = (imageRect.width - targetRect.width) / 2
                right = (targetRect.width + imageRect.width) / 2

            top = (imageRect.height - targetRect.height) / 2
            bottom = (targetRect.height + imageRect.height) / 2

            imageRect.x = max(imageRect.x, left)
            imageRect.y = max(imageRect.y, top)
            imageRect.width = min(imageRect.right, right) - imageRect.x
            imageRect.height = min(imageRect.bottom, bottom) - imageRect.y

        # if textureView.fitObject:
        #     imageSurf = pygame.transform.scale(imageSurf, (targetRect.width, targetRect.height))
        #     imageRect = imageSurf.get_rect()

        # convert to left-top oriented screen space according to alignment
        y = targetRect.y - imageRect.height / 2
        if textureView.halign == "left":
            x = targetRect.x - targetRect.width / 2
        elif textureView.halign == "right":
            x = targetRect.x + targetRect.width / 2 - imageRect.width
        else:
            x = targetRect.x - imageRect.width / 2

        self.surface.blit(imageSurf, (x, y), imageRect)
        return pygame.Rect(x, y, targetRect.width, targetRect.height)

    def drawImage(self, imageName, screenRect, imageRect=None, halign="center"):
        surf = self.resManager.getLoaded(imageName)
        if not imageRect:
            imageRect = surf.get_rect()

        y = screenRect.y - imageRect.height / 2
        if halign == "left":
            x = screenRect.x - screenRect.width / 2
        elif halign == "right":
            x = screenRect.x + screenRect.width / 2 - imageRect.width
        else:
            x = screenRect.x - imageRect.width / 2

        self.surface.blit(surf, (x, y), imageRect)

    def drawStretchedImage(self, imageName, screenRect, imageRect=None):
        surf = self.resManager.getLoaded(imageName)
        if not imageRect:
            imageRect = surf.get_rect()

        surf = pygame.transform.scale(surf, (screenRect.width, screenRect.height))
        rt = screenRect.copy()
        rt.center = (screenRect.x, screenRect.y)

        self.surface.blit(surf, (rt.x, rt.y), imageRect)

    def drawRect(self, color, rect):
        rt = rect.copy()
        rt.center = (rect.x, rect.y)
        pygame.draw.rect(self.surface, color, rt)

    def pprint(self, text, x, y, center=False, color=(0, 0, 0), scale=(1.0, 1.0)):
        self.resManager.createTextSurface(self.resManager.DEFAULT_FONT, self.resManager.DEFAULT_FONT_SIZE, color, "__pprint", text, True)
        surf = self.resManager.getLoaded("__pprint")
        rect = surf.get_rect()
        surf = pygame.transform.scale(surf, (int(scale[0] * rect.width), int(scale[1] * rect.height)))
        if center:
            x -= surf.get_width() / 2
            y -= surf.get_height() / 2
        self.surface.blit(surf, (x, y))

    def _distanceDivision(self, distance, rect):
        distanceFactor = 1 / distance
        rect.x      *= distanceFactor
        rect.y      *= distanceFactor
        rect.width  *= distanceFactor
        rect.height *= distanceFactor

