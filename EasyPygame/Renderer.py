from array import array
from OpenGL.GL import *
import glm

VSHADER = """
#version 330

layout(location=0) in vec4 pos;
layout(location=1) in vec2 texCoord;

uniform mat4 mvp;

out vec2 fragTexCoord;

void main(){
    gl_Position = mvp * pos;
    fragTexCoord = texCoord;
}
"""

VSHADER_INSTANCEDPOS = """
#version 330

layout(location=0) in vec4 pos;
layout(location=1) in vec2 texCoord;

uniform mat4 m;
uniform mat4 vp;
uniform float width;
uniform float height;
uniform int numInRow;

out vec2 fragTexCoord;

void main(){
    vec4 leftTop = m * pos;
    leftTop.x += (gl_InstanceID % numInRow) * width;
    leftTop.y -= (gl_InstanceID / numInRow) * height;

    gl_Position = vp * leftTop;
    fragTexCoord = texCoord;
}
"""

FSHADER_COLOR = """
#version 330

out vec4 fColor;

uniform vec4 color;

void main(){
    fColor = color;
}
"""

FSHADER_TEXTURE = """
#version 330

in vec2 fragTexCoord;
out vec4 fColor;

uniform sampler2D sampler;

void main(){
    vec4 sampled = texture(sampler, fragTexCoord);
    if (sampled.a < 1.0)
        discard;
    fColor = sampled;
}
"""

quadPositions = array('f', [
    0.5, 0.5,
    0.5, -0.5,
    -0.5, 0.5,
    -0.5, -0.5
]).tobytes()

class RendererOpenGL:
    def __init__(self, displaySurf, resManager):
        self.surface = displaySurf
        self.resManager = resManager

        self.toRenderDefaults = []
        self.toRenderTextured = []
        self.toRenderTexInstancedCluster = []

        self.pMat = glm.perspectiveFovRH(glm.radians(90), 500, 500, 0.1, 100)
        self.vpMat = None

        self.colorProgram = None
        self.textureProgram = None
        self.texInstancedPosProgram = None

        self.currBoundTex = None
        self.quadVBO = None
        self.quadTexCoords = None

        glClearColor(1.0, 1.0, 1.0, 1.0)
        self._initPrograms()
        self.colorMVPIndex = glGetUniformLocation(self.colorProgram, "mvp")
        self.colorColorIndex = glGetUniformLocation(self.colorProgram, "color")
        self.textureMVPIndex = glGetUniformLocation(self.textureProgram, "mvp")
        self.textureSamplerIndex = glGetUniformLocation(self.textureProgram, "sampler")
        self.TIPmIndex = glGetUniformLocation(self.texInstancedPosProgram, "m")
        self.TIPvpIndex = glGetUniformLocation(self.texInstancedPosProgram, "vp")
        self.TIPwidthIndex = glGetUniformLocation(self.texInstancedPosProgram, "width")
        self.TIPheightIndex = glGetUniformLocation(self.texInstancedPosProgram, "height")
        self.TIPnumInRowIndex = glGetUniformLocation(self.texInstancedPosProgram, "numInRow")
        self.TIPsamplerIndex = glGetUniformLocation(self.texInstancedPosProgram, "sampler")

        self._initBuffers()
        glUseProgram(self.colorProgram)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, None)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
        glUseProgram(self.textureProgram)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, None)
        glUseProgram(self.texInstancedPosProgram)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, None)

    def render(self, camera):
        self.vpMat = self.pMat * self._calcVMat(camera)

        if self.toRenderTexInstancedCluster:
            glUseProgram(self.texInstancedPosProgram)
            glUniformMatrix4fv(self.TIPvpIndex, 1, GL_FALSE, glm.value_ptr(self.vpMat))
            for obj in self.toRenderTexInstancedCluster:
                self._renderTexInstancedCluster(*obj)
                self.toRenderTexInstancedCluster = []

        if self.toRenderDefaults:
            glUseProgram(self.colorProgram)
            for obj in self.toRenderDefaults:
                self._renderDefault(*obj)
            self.toRenderDefaults = []

        if self.toRenderTextured:
            glUseProgram(self.textureProgram)
            for obj in self.toRenderTextured:
                self._renderTextured(*obj)
            self.toRenderTextured = []

    def _renderDefault(self, worldRect, color, name):
        worldMat = self._calcWorldMat(worldRect)
        mvpMat = self.vpMat * worldMat
        glUniformMatrix4fv(self.colorMVPIndex, 1, GL_FALSE, glm.value_ptr(mvpMat))
        glUniform4f(self.colorColorIndex, color[0], color[1], color[2], 1.0)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def renderDefault(self, worldRect, color, name):
        self.toRenderDefaults.append((worldRect, color, name))

    def renderTextured(self, worldRect, textureView):
        self.toRenderTextured.append((worldRect, textureView))

    def _textureUploadAttributes(self, textureView):
        texture = self.resManager.getTexture(textureView.texture)
        if texture != self.currBoundTex:
            glBindTexture(GL_TEXTURE_2D, texture)
            self.currBoundTex = texture
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        texRect = textureView.imageRect

        a = [
            texRect.x + texRect.width, texRect.y,
            texRect.x + texRect.width, texRect.y + texRect.height,
            texRect.x, texRect.y,
            texRect.x, texRect.y + texRect.height
        ]

        texCoords = array('f', a).tobytes()

        if textureView.flipX:
            texCoords[0], texCoords[1], texCoords[4], texCoords[5] = texCoords[4], texCoords[5], texCoords[0], texCoords[1]
            texCoords[2], texCoords[3], texCoords[6], texCoords[7] = texCoords[6], texCoords[7], texCoords[2], texCoords[3]

        if textureView.flipY:
            texCoords[0], texCoords[1], texCoords[2], texCoords[3] = texCoords[2], texCoords[3], texCoords[0], texCoords[1]
            texCoords[4], texCoords[5], texCoords[6], texCoords[7] = texCoords[6], texCoords[7], texCoords[4], texCoords[5]

        glBindBuffer(GL_ARRAY_BUFFER, self.quadTexCoords)
        glBufferSubData(GL_ARRAY_BUFFER, 0, None, texCoords)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

    def _renderTextured(self, worldRect, textureView):
        self._textureUploadAttributes(textureView)

        mvpMat = self.vpMat * self._calcWorldMat(worldRect)
        glUniformMatrix4fv(self.textureMVPIndex, 1, GL_FALSE, glm.value_ptr(mvpMat))

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def renderTexInstancedCluster(self, center, width, height, textureView, n):
        self.toRenderTexInstancedCluster.append((center, width, height, textureView, n))

    def _renderTexInstancedCluster(self, center, width, height, textureView, n):
        self._textureUploadAttributes(textureView)

        if n < 1:
            return
        tilePos = n // 2

        x = center[0] - width * tilePos
        y = center[1] + height * tilePos
        m = glm.translate(glm.mat4(), glm.vec3(x, y, 0))

        glUniformMatrix4fv(self.TIPmIndex, 1, GL_FALSE, glm.value_ptr(m))
        glUniform1f(self.TIPwidthIndex, width)
        glUniform1f(self.TIPheightIndex, height)
        glUniform1i(self.TIPnumInRowIndex, n)

        glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, n * n)

    def pprint(self, text, x, y, center=False, color=(0, 0, 0), scale=(1.0, 1.0)):
        pass

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def _createShader(shaderType, source):
        shader = glCreateShader(shaderType)
        glShaderSource(shader, source)
        glCompileShader(shader)
        error = glGetShaderInfoLog(shader)
        print(error)
        return shader

    @staticmethod
    def _createProgram(vshader, fshader):
        program = glCreateProgram()
        glAttachShader(program, vshader)
        glAttachShader(program, fshader)
        glLinkProgram(program)
        glDetachShader(program, vshader)
        glDetachShader(program, fshader)
        return program

    def _initPrograms(self):
        vshader = self._createShader(GL_VERTEX_SHADER, VSHADER)
        vshader_insPos = self._createShader(GL_VERTEX_SHADER, VSHADER_INSTANCEDPOS)
        fshader_color = self._createShader(GL_FRAGMENT_SHADER, FSHADER_COLOR)
        fshader_texture = self._createShader(GL_FRAGMENT_SHADER, FSHADER_TEXTURE)

        self.colorProgram = self._createProgram(vshader, fshader_color)
        self.textureProgram = self._createProgram(vshader, fshader_texture)
        self.texInstancedPosProgram = self._createProgram(vshader_insPos, fshader_texture)
        glDeleteShader(vshader)
        glDeleteShader(vshader_insPos)
        glDeleteShader(fshader_color)
        glDeleteShader(fshader_texture)

    def _initBuffers(self):
        self.quadVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
        glBufferData(GL_ARRAY_BUFFER, quadPositions, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)

        self.quadTexCoords = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.quadTexCoords)
        glBufferData(GL_ARRAY_BUFFER, quadPositions, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(1)

    def _calcMVPMat(self, cosntRect, constCamera):
        mvpMat = glm.mat4()
        mvpMat = glm.translate(mvpMat, glm.vec3(cosntRect.x, cosntRect.y, 0))
        mvpMat = glm.scale(mvpMat, glm.vec3(cosntRect.width, cosntRect.height, 1))
        vMat = glm.lookAt(glm.vec3(constCamera.pos[0], constCamera.pos[1], constCamera.distance), \
            glm.vec3(constCamera.pos[0], constCamera.pos[1], 0), glm.vec3(0, 1, 0))
        pMat = glm.perspectiveFovRH(glm.radians(90), 500, 500, 0.1, 100)
        return pMat * vMat * mvpMat

    def _calcWorldMat(self, worldRect):
        worldMat = glm.mat4()
        worldMat = glm.translate(worldMat, glm.vec3(worldRect.x, worldRect.y, 0))
        return glm.scale(worldMat, glm.vec3(worldRect.width, worldRect.height, 1))

    def _calcVMat(self, constCamera):
        return glm.lookAt(glm.vec3(constCamera.pos[0], constCamera.pos[1], constCamera.distance), \
            glm.vec3(constCamera.pos[0], constCamera.pos[1], 0), glm.vec3(0, 1, 0))


# class Renderer:
#     def __init__(self, displaySurf, resManager):
#         self.surface = displaySurf
#         self.resManager = resManager

#     def renderDefault(self, worldRect, camera, color, name):
#         # world
#         targetRect = worldRect

#         # view
#         targetRect.x, targetRect.y = camera.view([worldRect.x, worldRect.y])

#         # proj
#         self._distanceDivision(camera.distance, targetRect)

#         # screen space
#         targetRect.x += self.surface.get_width() / 2
#         targetRect.y = self.surface.get_height() / 2 - targetRect.y

#         self.drawRect(color, targetRect)
#         self.pprint(name, targetRect.x, targetRect.y, True, scale=(1 / camera.distance, 1 / camera.distance))

#         retRect = targetRect.copy()
#         retRect.center = (retRect.x, retRect.y)
#         return retRect

#     def renderTextured(self, worldRect, camera, textureView):
#         # +------------+---------+-------+----------------+
#         # | StretchFit | CropFit | Scale |   Destination  |
#         # +------------+---------+-------+----------------+
#         # |      0     |    0    |   0   |     source     |
#         # +------------+---------+-------+----------------+
#         # |      0     |    0    |   1   |  source scaled |
#         # +------------+---------+-------+----------------+
#         # |      0     |    1    |   0   |   crop to fit  |
#         # +------------+---------+-------+----------------+
#         # |      0     |    1    |   1   |   crop to fit  |
#         # |            |         |       |    and scale   |
#         # +------------+---------+-------+----------------+
#         # |      1     |    X    |   0   | stretch to fit |
#         # +------------+---------+-------+----------------+
#         # |      1     |    X    |   1   | stretch to fit |
#         # |            |         |       |    and scale   |
#         # +------------+---------+-------+----------------+

#         imageSurf = self.resManager.getLoaded(textureView.texture)
#         imageSurf = pygame.transform.flip(imageSurf, textureView.flipX, textureView.flipY)
#         if textureView.imageRect:
#             imageRect = textureView.imageRect.copy()
#             tempSurf = pygame.Surface((imageRect.width, imageRect.height), pygame.SRCALPHA)
#             tempSurf.fill((255, 255, 255, 0))
#             tempSurf.blit(imageSurf, (0, 0), imageRect)
#             imageSurf = tempSurf
#         # imageRect x y are now 0
#         imageRect = imageSurf.get_rect()

#         # world
#         targetRect = worldRect
#         scale = list(textureView.scale)

#         if not textureView.stretchFit and not textureView.cropFit:
#             targetRect.width, targetRect.height = (imageRect.width, imageRect.height)

#         # view
#         targetRect.x, targetRect.y = camera.view([worldRect.x, worldRect.y])

#         # proj
#         self._distanceDivision(camera.distance, targetRect)

#         # if stretchFit, image does not need to be scaled to distance.
#         # It will be stretched to gameOjbect later
#         if not textureView.stretchFit:
#             targetRect.width  *= scale[0]
#             targetRect.height *= scale[1]
#             imageSurfFactor = [1 / imageRect.width, 1 / imageRect.height]
#             self._distanceDivision(camera.distance, imageRect)
#             imageRect.width *= scale[0]
#             imageRect.height *= scale[1]
#             imageSurfFactor[0] *= imageRect.width
#             imageSurfFactor[1] *= imageRect.height
#             imageSurfRect = imageSurf.get_rect()
#             imageSurf = pygame.transform.scale(imageSurf, (int(imageSurfRect.width * imageSurfFactor[0]), int(imageSurfRect.height * imageSurfFactor[1])))

#         # convert to screen space
#         # targetRect is in screen space but with x y being its center
#         targetRect.x += self.surface.get_width() / 2
#         targetRect.y = self.surface.get_height() / 2 - targetRect.y

#         targetRect.x += textureView.relPos[0]
#         targetRect.y -= textureView.relPos[1]

#         if textureView.stretchFit:
#             thisScale = (targetRect.width / imageRect.width * scale[0], targetRect.height / imageRect.height * scale[1])
#             imageSurfRect = imageSurf.get_rect()
#             imageSurfRect.width *= thisScale[0]
#             imageSurfRect.height *= thisScale[1]
#             imageRect.width *= thisScale[0]
#             imageRect.height *= thisScale[1]
#             imageSurf = pygame.transform.scale(imageSurf, (imageSurfRect.width, imageSurfRect.height))
#         # convert targetRect to image space and find new imageRect for crop
#         elif textureView.cropFit:
#             if textureView.halign == "left":
#                 left = 0
#                 right = targetRect.width
#             elif textureView.halign == "right":
#                 right = imageRect.width
#                 left = right - targetRect.width
#             else:
#                 left = (imageRect.width - targetRect.width) / 2
#                 right = (targetRect.width + imageRect.width) / 2

#             top = (imageRect.height - targetRect.height) / 2
#             bottom = (targetRect.height + imageRect.height) / 2

#             imageRect.x = max(imageRect.x, left)
#             imageRect.y = max(imageRect.y, top)
#             imageRect.width = min(imageRect.right, right) - imageRect.x
#             imageRect.height = min(imageRect.bottom, bottom) - imageRect.y

#         # convert to left-top oriented screen space according to alignment
#         y = targetRect.y - imageRect.height / 2
#         if textureView.halign == "left":
#             x = targetRect.x - targetRect.width / 2
#         elif textureView.halign == "right":
#             x = targetRect.x + targetRect.width / 2 - imageRect.width
#         else:
#             x = targetRect.x - imageRect.width / 2

#         self.surface.blit(imageSurf, (x, y), imageRect)
#         return pygame.Rect(x, y, imageRect.width, imageRect.height)

#     def drawImage(self, imageName, screenRect, imageRect=None, halign="center"):
#         surf = self.resManager.getLoaded(imageName)
#         if not imageRect:
#             imageRect = surf.get_rect()

#         y = screenRect.y - imageRect.height / 2
#         if halign == "left":
#             x = screenRect.x - screenRect.width / 2
#         elif halign == "right":
#             x = screenRect.x + screenRect.width / 2 - imageRect.width
#         else:
#             x = screenRect.x - imageRect.width / 2

#         self.surface.blit(surf, (x, y), imageRect)

#     def drawStretchedImage(self, imageName, screenRect, imageRect=None):
#         surf = self.resManager.getLoaded(imageName)
#         if not imageRect:
#             imageRect = surf.get_rect()

#         surf = pygame.transform.scale(surf, (screenRect.width, screenRect.height))
#         rt = screenRect.copy()
#         rt.center = (screenRect.x, screenRect.y)

#         self.surface.blit(surf, (rt.x, rt.y), imageRect)

#     def drawRect(self, color, rect):
#         rt = rect.copy()
#         rt.center = (rect.x, rect.y)
#         pygame.draw.rect(self.surface, color, rt)

#     def pprint(self, text, x, y, center=False, color=(0, 0, 0), scale=(1.0, 1.0)):
#         self.resManager.createTextSurface(self.resManager.DEFAULT_FONT, self.resManager.DEFAULT_FONT_SIZE, color, "__pprint", text, True)
#         surf = self.resManager.getLoaded("__pprint")
#         rect = surf.get_rect()
#         surf = pygame.transform.scale(surf, (int(scale[0] * rect.width), int(scale[1] * rect.height)))
#         if center:
#             x -= surf.get_width() / 2
#             y -= surf.get_height() / 2
#         self.surface.blit(surf, (x, y))

#     def _distanceDivision(self, distance, rect):
#         distanceFactor = 1 / distance
#         rect.x      *= distanceFactor
#         rect.y      *= distanceFactor
#         rect.width  *= distanceFactor
#         rect.height *= distanceFactor

