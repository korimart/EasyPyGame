class Test:
    def __init__(self):
        print(self.__class__)

class TestChild(Test):
    def __init__(self):
        super().__init__()

t = Test()
tchild = TestChild()