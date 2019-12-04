import heapq
from array import array
from OpenGL.GL import *
import glm
from ctypes import c_void_p

import EasyPygame

MVPINDEX = 0
MINDEX = 0
VPINDEX = 1
WIDTHINDEX = 2
HEIGHTINDEX = 3
NUMINROWINDEX = 4
COLORINDEX = 7
SAMPLERINDEX = 7

VSHADER = """
#version 430

layout(location=0) in vec4 pos;
layout(location=1) in vec2 texCoord;

layout(location=0) uniform mat4 mvp;

out vec2 fragTexCoord;

void main(){
    gl_Position = mvp * pos;
    fragTexCoord = texCoord;
}
"""

VSHADER_INSTANCED_CLUSTER = """
#version 430

layout(location=0) in vec4 pos;
layout(location=1) in vec2 texCoord;

layout(location=0) uniform mat4 m;
layout(location=1) uniform mat4 vp;
layout(location=2) uniform float width;
layout(location=3) uniform float height;
layout(location=4) uniform int numInRow;

out vec2 fragTexCoord;

void main(){
    vec4 leftTop = m * pos;
    leftTop.x += (gl_InstanceID % numInRow) * width;
    leftTop.y -= (gl_InstanceID / numInRow) * height;

    gl_Position = vp * leftTop;
    fragTexCoord = texCoord;
}
"""

VSHADER_INSTANCED_INDIVI = """
#version 430

layout(location=0) in vec4 pos;
layout(location=1) in vec2 texCoord;
layout(location=2) in mat4 m; // vertexattribdivisor

layout(location=1) uniform mat4 vp;

out vec2 fragTexCoord;

void main(){
    gl_Position = vp * m * pos;
    fragTexCoord = texCoord;
}
"""

FSHADER_COLOR = """
#version 430

out vec4 fColor;

layout(location=7) uniform vec4 color;

void main(){
    fColor = color;
}
"""

FSHADER_TEXTURE = """
#version 430

in vec2 fragTexCoord;
out vec4 fColor;

layout(location=7) uniform sampler2D sampler;

void main(){
    vec4 sampled = texture(sampler, fragTexCoord);
    fColor = sampled;
}
"""

quadPositions = array('f', [
    0.5, 0.5,
    0.5, -0.5,
    -0.5, 0.5,
    -0.5, -0.5
]).tobytes()

# class RendererOpenGL:
#     def __init__(self, window, resManager):
#         self.surface = window.displaySurface
#         self.resManager = resManager

#         self.toRenderColors = []
#         self.toRenderColorIns = []
#         self.toRenderTextured = []
#         self.toRenderTexInstancedCluster = []
#         self.toRenderTexInstIndivi = []
#         self.toRenderBlendingTex = []
#         self.toRenderBlendingTexID = 0

#         self.pMat = glm.perspectiveFovRH(glm.radians(90), window.width, window.height, 0.1, 100)
#         self.vpMat = None

#         self.colorProgram = None
#         self.colorInsProgram = None
#         self.textureProgram = None
#         self.texInsClusProg = None
#         self.texInsIndiviProg = None
#         self._initPrograms()
#         self.programs = [self.colorProgram, self.colorInsProgram, self.textureProgram, self.texInsClusProg, self.texInsIndiviProg]
#         self.currProgram = None

#         self.currBoundTex = None
#         self.currBoundMinFilter = GL_NEAREST
#         self.currBoundMagFilter = GL_NEAREST
#         self.quadVBO = None
#         self.quadTexCoords = None
#         self.instIndiviWorlds = None

#         glClearColor(0.0, 0.0, 0.0, 1.0)
#         glEnable(GL_DEPTH_TEST)
#         self._initBuffers()
#         for program in self.programs:
#             glUseProgram(program)
#             glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
#             glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, None)
#             glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

#         # print(glGetIntegerv(GL_MAX_VERTEX_UNIFORM_COMPONENTS))

#     def render(self, camera):
#         self.vpMat = self.pMat * self._calcVMat(camera)

#         glEnableVertexAttribArray(2)
#         glEnableVertexAttribArray(3)
#         glEnableVertexAttribArray(4)
#         glEnableVertexAttribArray(5)

#         if self.toRenderTexInstancedCluster:
#             if not self.currProgram == self.texInsClusProg:
#                 self.currProgram = self.texInsClusProg
#                 glUseProgram(self.texInsClusProg)
#             glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.vpMat))
#             for obj in self.toRenderTexInstancedCluster:
#                 self._renderTexInstancedCluster(*obj)
#             self.toRenderTexInstancedCluster = []

#         if self.toRenderTexInstIndivi:
#             if not self.currProgram == self.texInsIndiviProg:
#                 self.currProgram = self.texInsIndiviProg
#                 glUseProgram(self.texInsIndiviProg)
#             glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.vpMat))
#             for obj in self.toRenderTexInstIndivi:
#                 self._renderTexInstancedIndivi(*obj)
#             self.toRenderTexInstIndivi = []

#         if self.toRenderColorIns:
#             if not self.currProgram == self.colorInsProgram:
#                 self.currProgram = self.colorInsProgram
#                 glUseProgram(self.colorInsProgram)
#             glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.vpMat))
#             for obj in self.toRenderColorIns:
#                 self._renderColorInstanced(*obj)
#             self.toRenderColorIns = []

#         glDisableVertexAttribArray(2)
#         glDisableVertexAttribArray(3)
#         glDisableVertexAttribArray(4)
#         glDisableVertexAttribArray(5)

#         if self.toRenderColors:
#             if not self.currProgram == self.colorProgram:
#                 self.currProgram = self.colorProgram
#                 glUseProgram(self.colorProgram)
#             for obj in self.toRenderColors:
#                 self._renderColor(*obj)
#             self.toRenderColors = []

#         if self.toRenderTextured:
#             if not self.currProgram == self.textureProgram:
#                 self.currProgram = self.textureProgram
#                 glUseProgram(self.textureProgram)
#             for obj in self.toRenderTextured:
#                 self._renderTextured(*obj)
#             self.toRenderTextured = []

#         glEnable(GL_BLEND)
#         glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#         if self.toRenderBlendingTex:
#             if not self.currProgram == self.textureProgram:
#                 self.currProgram = self.textureProgram
#                 glUseProgram(self.textureProgram)

#             while self.toRenderBlendingTex:
#                 _, withID = heapq.heappop(self.toRenderBlendingTex)
#                 obj = withID[1]
#                 self._renderTextured(*obj)

#         glDisable(GL_BLEND)

#     def _renderColor(self, worldRect, color, name):
#         worldMat = self._calcWorldMat(worldRect)
#         mvpMat = self.vpMat * worldMat
#         glUniformMatrix4fv(MVPINDEX, 1, GL_FALSE, glm.value_ptr(mvpMat))
#         glUniform4f(COLORINDEX, *color, 1.0)

#         glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

#     def renderColor(self, worldRect, color, name):
#         self.toRenderColors.append((worldRect, color, name))

#     def renderColorInstanced(self, worldRectList, color, name):
#         self.toRenderColorIns.append((worldRectList, color, name))

#     def _renderColorInstanced(self, worldRectList, color, name):
#         glUniform4f(COLORINDEX, *color, 1.0)
#         a = []
#         for worldRect in worldRectList[:1000]:
#             worldMat = self._calcWorldMat(worldRect)
#             for i in range(4):
#                 for j in range(4):
#                     a.append(worldMat[i][j])

#         data = array('f', a).tobytes()

#         glBindBuffer(GL_ARRAY_BUFFER, self.instIndiviWorlds)
#         glBufferSubData(GL_ARRAY_BUFFER, 0, None, data)

#         size = min(len(worldRectList), 1000)

#         glVertexAttribPointer(2, 4, GL_FLOAT, False, 16 * 4, c_void_p(0))
#         glVertexAttribPointer(3, 4, GL_FLOAT, False, 16 * 4, c_void_p(16))
#         glVertexAttribPointer(4, 4, GL_FLOAT, False, 16 * 4, c_void_p(32))
#         glVertexAttribPointer(5, 4, GL_FLOAT, False, 16 * 4, c_void_p(48))

#         glVertexAttribDivisor(2, 1)
#         glVertexAttribDivisor(3, 1)
#         glVertexAttribDivisor(4, 1)
#         glVertexAttribDivisor(5, 1)

#         glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, size)

#     def renderTextured(self, worldRect, textureView):
#         self.toRenderTextured.append((worldRect, textureView))

#     def _textureUploadAttributes(self, textureView):
#         texture = self.resManager.getTexture(textureView.texture)
#         minFilter = GL_LINEAR if textureView.minFilter == "linear" else GL_NEAREST
#         magFilter = GL_LINEAR if textureView.magFilter == "linear" else GL_NEAREST
#         if texture != self.currBoundTex:
#             glBindTexture(GL_TEXTURE_2D, texture)
#             self.currBoundTex = texture

#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
#         else:
#             if self.currBoundMinFilter != minFilter:
#                 glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
#                 self.currBoundMinFilter = minFilter
#             if self.currBoundMagFilter != magFilter:
#                 glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
#                 self.currBoundMagFilter = magFilter

#         texRect = textureView.imageRect

#         a = [
#             texRect.x + texRect.width, texRect.y,
#             texRect.x + texRect.width, texRect.y + texRect.height,
#             texRect.x, texRect.y,
#             texRect.x, texRect.y + texRect.height
#         ]

#         if textureView.flipX:
#             a[0], a[1], a[4], a[5] = a[4], a[5], a[0], a[1]
#             a[2], a[3], a[6], a[7] = a[6], a[7], a[2], a[3]

#         if textureView.flipY:
#             a[0], a[1], a[2], a[3] = a[2], a[3], a[0], a[1]
#             a[4], a[5], a[6], a[7] = a[6], a[7], a[4], a[5]

#         texCoords = array('f', a).tobytes()

#         glBindBuffer(GL_ARRAY_BUFFER, self.quadTexCoords)
#         glBufferSubData(GL_ARRAY_BUFFER, 0, None, texCoords)
#         glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

#     def _renderTextured(self, worldRect, textureView):
#         self._textureUploadAttributes(textureView)

#         mvpMat = self.vpMat * self._calcWorldMat(worldRect)
#         glUniformMatrix4fv(MVPINDEX, 1, GL_FALSE, glm.value_ptr(mvpMat))

#         glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

#     def renderTexInstancedCluster(self, center, width, height, textureView, n):
#         self.toRenderTexInstancedCluster.append((center, width, height, textureView, n))

#     def _renderTexInstancedCluster(self, center, width, height, textureView, n):
#         self._textureUploadAttributes(textureView)

#         if n < 1:
#             return
#         tilePos = n // 2

#         x = center[0] - width * tilePos
#         y = center[1] + height * tilePos
#         m = glm.translate(glm.mat4(), glm.vec3(x, y, center[2]))

#         glUniformMatrix4fv(MINDEX, 1, GL_FALSE, glm.value_ptr(m))
#         glUniform1f(WIDTHINDEX, width)
#         glUniform1f(HEIGHTINDEX, height)
#         glUniform1i(NUMINROWINDEX, n)

#         glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, n * n)

#     def _renderTexInstancedIndivi(self, worldRectList, textureView):
#         self._textureUploadAttributes(textureView)
#         a = []
#         for worldRect in worldRectList[:1000]:
#             worldMat = self._calcWorldMat(worldRect)
#             for i in range(4):
#                 for j in range(4):
#                     a.append(worldMat[i][j])

#         data = array('f', a).tobytes()

#         glBindBuffer(GL_ARRAY_BUFFER, self.instIndiviWorlds)
#         glBufferSubData(GL_ARRAY_BUFFER, 0, None, data)

#         size = min(len(worldRectList), 1000)

#         glVertexAttribPointer(2, 4, GL_FLOAT, False, 16 * 4, c_void_p(0))
#         glVertexAttribPointer(3, 4, GL_FLOAT, False, 16 * 4, c_void_p(16))
#         glVertexAttribPointer(4, 4, GL_FLOAT, False, 16 * 4, c_void_p(32))
#         glVertexAttribPointer(5, 4, GL_FLOAT, False, 16 * 4, c_void_p(48))

#         glVertexAttribDivisor(2, 1)
#         glVertexAttribDivisor(3, 1)
#         glVertexAttribDivisor(4, 1)
#         glVertexAttribDivisor(5, 1)

#         glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, size)

#     def renderTexInstancedIndivi(self, worldRectList, textureView):
#         self.toRenderTexInstIndivi.append((worldRectList, textureView))

#     def renderBlendingTexture(self, worldRect, textureView, priority):
#         heapq.heappush(self.toRenderBlendingTex, (priority, (self.toRenderBlendingTexID, (worldRect, textureView))))
#         self.toRenderBlendingTexID += 1

#     def pprint(self, text, x, y, center=False, color=(0, 0, 0), scale=(1.0, 1.0)):
#         pass

#     def clear(self):
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

#     @staticmethod
#     def _createShader(shaderType, source):
#         shader = glCreateShader(shaderType)
#         glShaderSource(shader, source)
#         glCompileShader(shader)
#         print(glGetShaderInfoLog(shader))
#         return shader

#     @staticmethod
#     def _createProgram(vshader, fshader):
#         program = glCreateProgram()
#         glAttachShader(program, vshader)
#         glAttachShader(program, fshader)
#         glLinkProgram(program)
#         print(glGetProgramInfoLog(program))
#         glDetachShader(program, vshader)
#         glDetachShader(program, fshader)
#         return program

#     def _initPrograms(self):
#         vshader = self._createShader(GL_VERTEX_SHADER, VSHADER)
#         vshader_insClus = self._createShader(GL_VERTEX_SHADER, VSHADER_INSTANCED_CLUSTER)
#         vshader_insIndivi = self._createShader(GL_VERTEX_SHADER, VSHADER_INSTANCED_INDIVI)
#         fshader_color = self._createShader(GL_FRAGMENT_SHADER, FSHADER_COLOR)
#         fshader_texture = self._createShader(GL_FRAGMENT_SHADER, FSHADER_TEXTURE)

#         self.colorProgram = self._createProgram(vshader, fshader_color)
#         self.colorInsProgram = self._createProgram(vshader_insIndivi, fshader_color)
#         self.textureProgram = self._createProgram(vshader, fshader_texture)
#         self.texInsClusProg = self._createProgram(vshader_insClus, fshader_texture)
#         self.texInsIndiviProg = self._createProgram(vshader_insIndivi, fshader_texture)
#         glDeleteShader(vshader)
#         glDeleteShader(vshader_insClus)
#         glDeleteShader(vshader_insIndivi)
#         glDeleteShader(fshader_color)
#         glDeleteShader(fshader_texture)

#     def _initBuffers(self):
#         self.quadVBO = glGenBuffers(1)
#         glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
#         glBufferData(GL_ARRAY_BUFFER, quadPositions, GL_STATIC_DRAW)
#         glEnableVertexAttribArray(0)

#         self.quadTexCoords = glGenBuffers(1)
#         glBindBuffer(GL_ARRAY_BUFFER, self.quadTexCoords)
#         glBufferData(GL_ARRAY_BUFFER, quadPositions, GL_DYNAMIC_DRAW)
#         glEnableVertexAttribArray(1)

#         self.instIndiviWorlds = glGenBuffers(1)
#         glBindBuffer(GL_ARRAY_BUFFER, self.instIndiviWorlds)
#         glBufferData(GL_ARRAY_BUFFER, 16 * 4 * 1000, None, GL_DYNAMIC_DRAW)


#     @staticmethod
#     def _calcMVPMat(constRect, constCamera):
#         mvpMat = glm.mat4()
#         mvpMat = glm.translate(mvpMat, glm.vec3(constRect.x, constRect.y, constRect.z))
#         mvpMat = glm.scale(mvpMat, glm.vec3(constRect.width, constRect.height, 1))
#         vMat = glm.lookAt(glm.vec3(constCamera.pos[0], constCamera.pos[1], constCamera.distance), \
#             glm.vec3(constCamera.pos[0], constCamera.pos[1], 0), glm.vec3(0, 1, 0))
#         pMat = glm.perspectiveFovRH(glm.radians(90), 500, 500, 0.1, 100)
#         return pMat * vMat * mvpMat

#     @staticmethod
#     def _calcWorldMat(worldRect):
#         worldMat = glm.mat4()
#         worldMat = glm.translate(worldMat, glm.vec3(worldRect.x, worldRect.y, worldRect.z))
#         return glm.scale(worldMat, glm.vec3(worldRect.width, worldRect.height, 1))

#     @staticmethod
#     def _calcVMat(constCamera):
#         return glm.lookAt(glm.vec3(constCamera.pos[0], constCamera.pos[1], constCamera.distance), \
#             glm.vec3(constCamera.pos[0], constCamera.pos[1], 0), glm.vec3(0, 1, 0))

class Renderer:
    def __init__(self, window, resManager):
        self.resManager = resManager

        self.colorProgram = None
        self.colorInsProgram = None
        self.textureProgram = None
        self.textureInsProgram = None
        self._initPrograms()
        self.programs = [self.colorInsProgram, self.colorInsProgram, \
            self.textureProgram, self.textureInsProgram]

        self.quadVBO = None
        self.quadTexCoords = None
        self._initBuffers()

        for program in self.programs:
            glUseProgram(program)
            glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
            glVertexAttribPointer(0, 2, GL_FLOAT, False, 0, None)
            glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

        self.p = glm.perspectiveFovRH(glm.radians(90), window.width, window.height, 0.1, 100)
        self.pv = None
        self.colors = []
        self.colorIns = []
        self.textures = []
        self.texIns = []
        self.texBlending = []
        self.texInsBlending = []

        self.blending = False
        self.flipX = False
        self.flipY = False
        self.minFilter = "nearest"
        self.magFilter = "nearest"

        self.bufferInsNum = dict()
        self.currProgram = None
        self.currBoundTex = None
        self.currBoundMinFilter = GL_NEAREST
        self.currBoundMagFilter = GL_NEAREST

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def render(self, camera):
        self.pv = self.p * self._calcVMat(camera)

        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glEnableVertexAttribArray(4)
        glEnableVertexAttribArray(5)

        if self._useProgram(self.colorIns, self.colorInsProgram):
            glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.pv))
            self._flush(self.colorIns, self._renderColorInstanced)

        if self._useProgram(self.texIns, self.textureInsProgram):
            glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.pv))
            self._flush(self.texIns, self._renderTextureInstanced)

        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glDisableVertexAttribArray(4)
        glDisableVertexAttribArray(5)

        if self._useProgram(self.colors, self.colorProgram):
            self._flush(self.colors, self._renderColor)

        if self._useProgram(self.textures, self.textureProgram):
            self._flush(self.textures, self._renderTexture)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if self._useProgram(self.texBlending, self.textureProgram):
            self._flush(self.texBlending, self._renderTexture)

        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glEnableVertexAttribArray(4)
        glEnableVertexAttribArray(5)

        if self._useProgram(self.texInsBlending, self.textureInsProgram):
            glUniformMatrix4fv(VPINDEX, 1, GL_FALSE, glm.value_ptr(self.pv))
            self._flush(self.texInsBlending, self._renderTextureInstanced)

        glDisable(GL_BLEND)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def enableBlending(self):
        self.blending = True

    def disableBlending(self):
        self.blending = False

    def resetSettings(self):
        self.blending = False
        self.flipX = False
        self.flipY = False
        self.minFilter = "nearest"
        self.magFilter = "nearest"

    def renderColor(self, world, color):
        self.colors.append((world, color))

    def renderColorInstanced(self, bufferID, color, instNum):
        self.colorIns.append((bufferID, color, instNum))

    def setFilter(self, minFilter="nearest", magFilter="nearest"):
        if minFilter is not None:
            self.minFilter = minFilter
        if magFilter is not None:
            self.magFilter = magFilter

    def setFlip(self, x=True, y=True):
        if x is not None:
            self.flipX = x
        if y is not None:
            self.flipY = y

    def renderTexture(self, world, texture, texCoord=None):
        if self.blending:
            self.texBlending.append((self.minFilter, self.magFilter, self.flipX, self.flipY, world, texture, texCoord))
        else:
            self.textures.append((self.minFilter, self.magFilter, self.flipX, self.flipY, world, texture, texCoord))

    def renderTextureInstanced(self, bufferID, instNum, texture, texCoord=None):
        if self.blending:
            self.texInsBlending.append((self.minFilter, self.magFilter, self.flipX, self.flipY, bufferID, texture, texCoord, instNum))
        else:
            self.texIns.append((self.minFilter, self.magFilter, self.flipX, self.flipY, bufferID, texture, texCoord, instNum))

    def setInstancingWorlds(self, worldList, num=None, static=True):
        ret = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, ret)

        if worldList:
            a = []
            for world in worldList:
                worldMat = world
                for i in range(4):
                    for j in range(4):
                        a.append(worldMat[i][j])

            data = array('f', a).tobytes()

            if static:
                glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
            else:
                glBufferData(GL_ARRAY_BUFFER, data, GL_DYNAMIC_DRAW)

        elif num:
            if static:
                glBufferData(GL_ARRAY_BUFFER, 16 * 4 * num, None, GL_STATIC_DRAW)
            else:
                glBufferData(GL_ARRAY_BUFFER, 16 * 4 * num, None, GL_DYNAMIC_DRAW)

        else:
            return


        return ret

    def updateInstancingWorlds(self, bufferID, offset, worldList):
        a = []
        for world in worldList:
            for i in range(4):
                for j in range(4):
                    a.append(world[i][j])

        data = array('f', a).tobytes()

        glBindBuffer(GL_ARRAY_BUFFER, bufferID)
        glBufferSubData(GL_ARRAY_BUFFER, 16 * 4 * offset, None, data)

    def deleteBuffer(self, bufferID):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDeleteBuffers(1, bufferID)

    def _useProgram(self, radixList, program):
        if radixList:
            if not self.currProgram == program:
                self.currProgram = program
                glUseProgram(program)
            return True
        return False

    def _flush(self, radixList, func):
        for obj in radixList:
            func(*obj)
        del radixList[:]

    def _renderColor(self, world, color):
        world = world
        pvw = self.pv * world
        glUniformMatrix4fv(MVPINDEX, 1, GL_FALSE, glm.value_ptr(pvw))
        glUniform4f(COLORINDEX, *color, 1.0)

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def _renderColorInstanced(self, bufferID, color, instNum):
        glUniform4f(COLORINDEX, *color, 1.0)
        self._bindAndDrawIns(bufferID, instNum)

    def _renderTexture(self, minF, magF, flipX, flipY, world, texture, texCoord):
        self._textureUploadAttributes(minF, magF, flipX, flipY, texture, texCoord)
        mvpMat = self.pv * world
        glUniformMatrix4fv(MVPINDEX, 1, GL_FALSE, glm.value_ptr(mvpMat))

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def _renderTextureInstanced(self, minF, magF, flipX, flipY, bufferID, texture, texCoord, instNum):
        self._textureUploadAttributes(minF, magF, flipX, flipY, texture, texCoord)
        self._bindAndDrawIns(bufferID, instNum)

    def _bindAndDrawIns(self, bufferID, instNum):
        glBindBuffer(GL_ARRAY_BUFFER, bufferID)

        glVertexAttribPointer(2, 4, GL_FLOAT, False, 16 * 4, c_void_p(0))
        glVertexAttribPointer(3, 4, GL_FLOAT, False, 16 * 4, c_void_p(16))
        glVertexAttribPointer(4, 4, GL_FLOAT, False, 16 * 4, c_void_p(32))
        glVertexAttribPointer(5, 4, GL_FLOAT, False, 16 * 4, c_void_p(48))

        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glVertexAttribDivisor(4, 1)
        glVertexAttribDivisor(5, 1)

        glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, instNum)

    def _textureUploadAttributes(self, minFilter, magFilter, flipX, flipY, tex, texCoord):
        texture = self.resManager.getTexture(tex)
        minFilter = GL_LINEAR if minFilter == "linear" else GL_NEAREST
        magFilter = GL_LINEAR if magFilter == "linear" else GL_NEAREST
        if texture != self.currBoundTex:
            glBindTexture(GL_TEXTURE_2D, texture)
            self.currBoundTex = texture

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        else:
            if self.currBoundMinFilter != minFilter:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minFilter)
                self.currBoundMinFilter = minFilter
            if self.currBoundMagFilter != magFilter:
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magFilter)
                self.currBoundMagFilter = magFilter

        texRect = texCoord
        if not texRect:
            texRect = EasyPygame.EasyPygameRect(0, 0, 1, 1)

        a = [
            texRect.x + texRect.width, texRect.y,
            texRect.x + texRect.width, texRect.y + texRect.height,
            texRect.x, texRect.y,
            texRect.x, texRect.y + texRect.height
        ]

        if flipX:
            a[0], a[1], a[4], a[5] = a[4], a[5], a[0], a[1]
            a[2], a[3], a[6], a[7] = a[6], a[7], a[2], a[3]

        if flipY:
            a[0], a[1], a[2], a[3] = a[2], a[3], a[0], a[1]
            a[4], a[5], a[6], a[7] = a[6], a[7], a[4], a[5]

        texCoords = array('f', a).tobytes()

        glBindBuffer(GL_ARRAY_BUFFER, self.quadTexCoords)
        glBufferSubData(GL_ARRAY_BUFFER, 0, None, texCoords)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

    def _initPrograms(self):
        vshader = self._createShader(GL_VERTEX_SHADER, VSHADER)
        vshader_ins = self._createShader(GL_VERTEX_SHADER, VSHADER_INSTANCED_INDIVI)
        fshader_color = self._createShader(GL_FRAGMENT_SHADER, FSHADER_COLOR)
        fshader_texture = self._createShader(GL_FRAGMENT_SHADER, FSHADER_TEXTURE)

        self.colorProgram = self._createProgram(vshader, fshader_color)
        self.colorInsProgram = self._createProgram(vshader_ins, fshader_color)
        self.textureProgram = self._createProgram(vshader, fshader_texture)
        self.textureInsProgram = self._createProgram(vshader_ins, fshader_texture)
        glDeleteShader(vshader)
        glDeleteShader(vshader_ins)
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

    @staticmethod
    def _createShader(shaderType, source):
        shader = glCreateShader(shaderType)
        glShaderSource(shader, source)
        glCompileShader(shader)
        print(glGetShaderInfoLog(shader))
        return shader

    @staticmethod
    def _createProgram(vshader, fshader):
        program = glCreateProgram()
        glAttachShader(program, vshader)
        glAttachShader(program, fshader)
        glLinkProgram(program)
        print(glGetProgramInfoLog(program))
        glDetachShader(program, vshader)
        glDetachShader(program, fshader)
        return program

    @staticmethod
    def _calcVMat(constCamera):
        return glm.lookAt(glm.vec3(constCamera.pos[0], constCamera.pos[1], constCamera.distance), \
            glm.vec3(constCamera.pos[0], constCamera.pos[1], 0), glm.vec3(0, 1, 0))
