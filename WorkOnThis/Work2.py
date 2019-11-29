# __len__은 파이썬 문법 참고
class DSQueue:
    def push(self, item):
        # implement this
        pass

    def pop(self):
        # implement this
        pass

    def __len__(self):
        # implement this
        pass

class DSStack:
    def push(self, item):
        # implement this
        pass

    def pop(self):
        # implement this
        pass

    def __len__(self):
        # implement this
        pass

# push와 pop interface를 지원하는 자료구조(queue and stack)를 받아 maxBytes 이상이 사용되면 memCallback을 호출한다.
# dataStructure의 push pop 기능을 그대로 제공해야한다. (이미 써놓음)
# refer to GoF Decorator or Chain of Responsibility pattern
class DSAdaptivePushPop:
    def __init__(self, dataStructure, maxBytes, memCallback):
        self.dataStructure = dataStructure
        self.maxBytes = maxBytes
        self.memCallback = memCallback

    def push(self, item):
        # implement this
        self.dataStructure.push(item)

    def pop(self):
        # implement this
        popped = self.dataStructure.pop()
        return popped