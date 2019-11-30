class DSFactory:
    def getQueue(self):
        return DSQueue()

    def getStack(self):
        return DSStack()

    def getGraph(self):
        pass

class AdaptiveDSFactory:
    def __init__(self, maxBytes, memCallback):
        self.maxBytes = maxBytes
        self.memCallback = memCallback

    def getQueue(self):
        return DSAdaptivePushPop(DSQueue(), self.maxBytes, self.memCallback)

    def getStack(self):
        return DSAdaptivePushPop(DSStack(), self.maxBytes, self.memCallback)

    def getGraph(self):
        pass

# __len__은 파이썬 문법 참고
class DSQueue:
    def __init__(self):
        self.queue = []

    def push(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)

    def peek(self):
        return self.queue[0]

    def getList(self):
        return self.queue

class DSStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop(-1)

    def __len__(self):
       return len(self.stack)

    def peek(self):
        return self.stack[-1]

    def getList(self):
        return self.stack

# push와 pop interface를 지원하는 자료구조(queue and stack)를 받아 maxBytes 이상이 사용되면 memCallback을 호출한다.
# dataStructure의 push pop 기능을 그대로 제공해야한다. (이미 써놓음)
# refer to GoF Decorator or Chain of Responsibility pattern

from pympler import asizeof

class DSAdaptivePushPop:
    def __init__(self, dataStructure, maxBytes, memCallback):
        self.dataStructure = dataStructure
        self.maxBytes = maxBytes
        self.memCallback = memCallback

    def push(self, item):
        # implement this
        self.dataStructure.push(item)
        if (asizeof.asizeof(self.dataStructure) > self.maxBytes):
            self.memCallback()

    def pop(self):
        # implement this
        popped = self.dataStructure.pop()
        return popped

    def __len__(self):
       return len(self.dataStructure)

    def peek(self):
        return self.dataStructure.peek()

    def getList(self):
        return self.dataStructure.getList()