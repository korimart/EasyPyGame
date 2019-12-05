import pygame

class Input:
    def __init__(self):
        self.lastInputList = []
        self.thisInputList = []
        self.thisInputEnabled = dict()

    def isDown(self, inp : str):
        try:
            pychar = self.EasyPygameStrings[inp]
            return pychar in self.thisInputList and self.thisInputEnabled[pychar]
        except:
            raise Exception("input string not supported")

    def isDown1stTime(self, inp):
        try:
            pychar = self.EasyPygameStrings[inp]
            return pychar in self.thisInputList and self.thisInputEnabled[pychar] and pychar not in self.lastInputList
        except:
            raise Exception("input string not supported")

    def getPrintables(self):
        printables = []
        for pychar in self.thisInputList:
            if self.thisInputEnabled[pychar] and pychar not in self.lastInputList:
                string = self._getPrintableString(pychar)
                if string:
                    printables.append(string)
        return printables

    def _getPrintableString(self, pychar):
        shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
        caps = pygame.key.get_mods() & pygame.KMOD_CAPS
        capitalize = bool(caps) != bool(shift)
        try:
            string : str = self.PyChars[pychar]
            if capitalize:
                if string == "9":
                    string = "("
                elif string == "0":
                    string = ")"
                else:
                    string = string.upper()
        except:
            return None

        if len(string) == 1:
            return string
        elif string.startswith("KP"):
            return string[2:]

        return None

    def consume(self, inp):
        try:
            pychar = self.EasyPygameStrings[inp]
        except:
            raise Exception("input string not supported")

        try:
            self.thisInputEnabled[pychar] = False
        except:
            pass

    def register(self, inp):
        if inp not in self.thisInputList:
            self.thisInputList.append(inp)

    def unregister(self, inp):
        try:
            self.thisInputList.remove(inp)
        except:
            pass

    def enableInput(self):
        self.thisInputEnabled = {inp : True for inp in self.thisInputList}

    def tick(self):
        self.lastInputList = self.thisInputList[:]

    PyChars = {
        pygame.K_KP0         : "KP0",
        pygame.K_KP1         : "KP1",
        pygame.K_KP2         : "KP2",
        pygame.K_KP3         : "KP3",
        pygame.K_KP4         : "KP4",
        pygame.K_KP5         : "KP5",
        pygame.K_KP6         : "KP6",
        pygame.K_KP7         : "KP7",
        pygame.K_KP8         : "KP8",
        pygame.K_KP9         : "KP9",
        pygame.K_KP_PERIOD   : "KP.",
        pygame.K_KP_DIVIDE   : "KP/",
        pygame.K_KP_MULTIPLY : "KP*",
        pygame.K_KP_MINUS    : "KP-",
        pygame.K_KP_PLUS     : "KP+",
        pygame.K_KP_EQUALS   : "KP=",
        pygame.K_a           : "a",
        pygame.K_b           : "b",
        pygame.K_c           : "c",
        pygame.K_d           : "d",
        pygame.K_e           : "e",
        pygame.K_f           : "f",
        pygame.K_g           : "g",
        pygame.K_h           : "h",
        pygame.K_i           : "i",
        pygame.K_j           : "j",
        pygame.K_k           : "k",
        pygame.K_l           : "l",
        pygame.K_m           : "m",
        pygame.K_n           : "n",
        pygame.K_o           : "o",
        pygame.K_p           : "p",
        pygame.K_q           : "q",
        pygame.K_r           : "r",
        pygame.K_s           : "s",
        pygame.K_t           : "t",
        pygame.K_u           : "u",
        pygame.K_v           : "v",
        pygame.K_w           : "w",
        pygame.K_x           : "x",
        pygame.K_y           : "y",
        pygame.K_z           : "z",
        pygame.K_0           : "0",
        pygame.K_1           : "1",
        pygame.K_2           : "2",
        pygame.K_3           : "3",
        pygame.K_4           : "4",
        pygame.K_5           : "5",
        pygame.K_6           : "6",
        pygame.K_7           : "7",
        pygame.K_8           : "8",
        pygame.K_9           : "9",
        pygame.K_COLON       : ":",
        pygame.K_SEMICOLON   : ";",
        pygame.K_LESS        : "<",
        pygame.K_EQUALS      : "=",
        pygame.K_GREATER     : ">",
        pygame.K_QUESTION    : "?",
        pygame.K_AT          : "@",
        pygame.K_LEFTBRACKET : "[",
        pygame.K_BACKSLASH   : "\\",
        pygame.K_RIGHTBRACKET: "]",
        pygame.K_CARET       : "^",
        pygame.K_UNDERSCORE  : "_",
        pygame.K_BACKQUOTE   : "`",
        pygame.K_SPACE       : " ",
        pygame.K_EXCLAIM     : "!",
        pygame.K_QUOTEDBL    : "\"",
        pygame.K_HASH        : "#",
        pygame.K_DOLLAR      : "$",
        pygame.K_AMPERSAND   : "&",
        pygame.K_QUOTE       : "'",
        pygame.K_LEFTPAREN   : "(",
        pygame.K_RIGHTPAREN  : ")",
        pygame.K_ASTERISK    : "*",
        pygame.K_PLUS        : "+",
        pygame.K_COMMA       : ",",
        pygame.K_MINUS       : "-",
        pygame.K_PERIOD      : ".",
        pygame.K_SLASH       : "/",
        pygame.K_BACKSPACE   : "BACKSPACE",
        pygame.K_RETURN      : "RETURN",
        1                    : "MOUSELEFT",
        2                    : "MOUSEMIDDLE",
        3                    : "MOUSERIGHT"
    }

    EasyPygameStrings = {value : key for key, value in PyChars.items()}