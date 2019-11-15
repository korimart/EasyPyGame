import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, fitObject=True, crop=False, halign="center", relPos=(0, 0)):
        self.texture = texture
        self.imageRect = imageRect
        self.fitObject = fitObject
        self.crop = crop
        self.relPos = relPos
        self.halign = halign

    def render(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])

        # rect has been converted to screen space
        rect.x = x + self.relPos[0]
        rect.y = y - self.relPos[1]

        if self.fitObject:
            EasyPygame.drawStretchedImage(self.texture, rect, self.imageRect)
            return

        imageSurf = EasyPygame._getImageSurf(self.texture)
        if not self.imageRect:
            imageRect = imageSurf.get_rect().copy()

        imageHalfWidth = imageSurf.get_width() / 2
        imageHalfHeight = imageSurf.get_height() / 2

        # convert to imageRect coordinate and translate
        if self.crop:
            if self.align == "left":
                left = 0
                right = rect.width
            elif self.align == "right":
                right = imageHalfWidth * 2
                left = right - rect.width
            else:
                left = imageHalfWidth - rect.width / 2
                right = rect.width / 2 + imageHalfWidth

            top = imageHalfHeight - rect.height / 2
            bottom = rect.height / 2 + imageHalfHeight

            imageRect.x = max(imageRect.x, left)
            imageRect.y = max(imageRect.y, top)
            imageRect.width = min(imageRect.right, right) - imageRect.x
            imageRect.height = min(imageRect.bottom, bottom) - imageRect.y

        EasyPygame.drawImage(self.texture, rect, imageRect, self.halign)

class DefaultTextureView:
    def __init__(self, color=(0, 0, 255)):
        self.color = color

    def render(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y
        EasyPygame.drawRect(self.color, rect)
        EasyPygame.pprint(gameObject.name, x, y, True)
