import EasyPygame

class TextureView:
    def __init__(self, texture, imageRect=None, fitObject=True, crop=False, align="center", relPos=(0, 0)):
        self.texture = texture
        self.imageRect = imageRect
        self.fitObject = fitObject
        self.crop = crop
        self.relPos = relPos
        self.align = align

    def render(self, gameObject, camera):
        rect = gameObject.rect.copy()
        x, y = camera.view([rect.x, rect.y])
        rect.x = x
        rect.y = y

        if self.fitObject:
            EasyPygame.drawStretchedImage(self.texture, rect, self.imageRect)
            return
            
        imageSurf = EasyPygame._getImageSurf(self.texture)
        if not self.imageRect:
            imageRect = imageSurf.get_rect().copy()

        if self.crop:
            imageHalfWidth = imageSurf.get_width() / 2
            imageHalfHeight = imageSurf.get_height() / 2

            # convert to imageRect coordinate and translate
            left = (rect.x - rect.width / 2) - rect.x + imageHalfWidth + self.relPos[0]
            right = (rect.x + rect.width / 2) - rect.x + imageHalfWidth + self.relPos[0]
            top = rect.y - (rect.y + rect.height / 2) + imageHalfHeight + self.relPos[1]
            bottom = rect.y - (rect.y - rect.height / 2) + imageHalfHeight + self.relPos[1]
            
            # crop
            imageRect.x = max(imageRect.x, left)
            imageRect.y = max(imageRect.y, top)
            imageRect.width = min(imageRect.right, right) - imageRect.x
            imageRect.height = min(imageRect.bottom, bottom) - imageRect.y

        if self.crop:
            EasyPygame.drawImage(self.texture, rect, imageRect)
        else:
            EasyPygame.drawImage(self.texture, rect, self.imageRect)
                
        

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
