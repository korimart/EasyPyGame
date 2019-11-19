import pygame

class Renderer:
    def __init__(self, displaySurf, resManager):
        self.surface = displaySurf
        self.resManager = resManager

    def render(self, worldRect, camera, textureView):
        imageSurf = self.resManager.getLoaded(textureView.texture)
        if not textureView.imageRect:
            imageRect = imageSurf.get_rect().copy()

        # world
        targetRect = worldRect

        if not textureView.fitObject and not textureView.crop:
            targetRect.width, targetRect.height = (imageRect.width, imageRect.height)

        targetRect.width  *= textureView.scale[0]
        targetRect.height *= textureView.scale[1]
        imageRect.width   *= textureView.scale[0]
        imageRect.height  *= textureView.scale[1]

        # view
        targetRect.x, targetRect.y = camera.view([worldRect.x, worldRect.y])

        # targetRect is in screen space but with x y being its center
        targetRect.x += textureView.relPos[0]
        targetRect.y -= textureView.relPos[1]

        # convert to imageRect coordinate and translate
        if textureView.crop:
            if textureView.align == "left":
                left = 0
                right = targetRect.width
            elif textureView.align == "right":
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

        if textureView.fitObject:
            self.drawStretchedImage(textureView.texture, targetRect, imageRect)
        else:
            self.drawImage(textureView.texture, targetRect, imageRect, textureView.align)

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
