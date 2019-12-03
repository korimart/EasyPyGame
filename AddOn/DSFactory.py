import time

class DSFactory:
    def getQueue(self):
        return DSQueue()

    def getStack(self):
        return DSStack()

    def getGraph(self):
        pass

class MemCheckDSFactory:
    def __init__(self, dsFactory, maxBytes, memCallback):
        self.dsFactory = dsFactory
        self.maxBytes = maxBytes
        self.memCallback = memCallback

    def getQueue(self):
        queue = self.dsFactory.getQueue()
        return PushPopMemCheckWrapper(queue, self.maxBytes, self.memCallback)

    def getStack(self):
        stack = self.dsFactory.getStack()
        return PushPopMemCheckWrapper(stack, self.maxBytes, self.memCallback)

    def getGraph(self):
        pass

class TimeCheckDSFactory:
    def __init__(self, dsFactory, maxMS, exception):
        self.dsFactory = dsFactory
        self.maxMS = maxMS
        self.exception = exception

    def getQueue(self):
        queue = self.dsFactory.getQueue()
        return PushPopTimeCheckWrapper(queue, self.maxMS, self.exception)

    def getStack(self):
        stack = self.dsFactory.getStack()
        return PushPopTimeCheckWrapper(stack, self.maxMS, self.exception)

    def getGraph(self):
        pass

class InsertCallbackDSFactory:
    def __init__(self, dsFactory, callback):
        self.dsFactory = dsFactory
        self.callback = callback

    def getQueue(self):
        queue = self.dsFactory.getQueue()
        return PushPopPushCheckWrapper(queue, self.callback)

    def getStack(self):
        stack = self.dsFactory.getStack()
        return PushPopPushCheckWrapper(stack, self.callback)

    def getGraph(self):
        pass

class DSSet:
    def __init(self):
        self.set = set()
    def add(self, item):
        self.set.add(item)
    def 


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

class PushPopWrapper:
    def __init__(self, dataStructure):
        self.dataStructure = dataStructure

    def push(self, item):
        self.dataStructure.push(item)

    def pop(self):
        popped = self.dataStructure.pop()
        return popped

    def __len__(self):
       return len(self.dataStructure)

    def peek(self):
        return self.dataStructure.peek()

    def getList(self):
        return self.dataStructure.getList()

class PushPopMemCheckWrapper(PushPopWrapper):
    def __init__(self, dataStructure, maxBytes, memCallback):
        super().__init__(dataStructure)
        self.maxBytes = maxBytes
        self.memCallback = memCallback

    def push(self, item):
        super().push(item)
        if (asizeof.asizeof(self.dataStructure) > self.maxBytes):
            self.memCallback()

class PushPopPushCheckWrapper(PushPopWrapper):
    def __init__(self, dataStructure, callBack):
        super().__init__(dataStructure)
        self.callBack = callBack

    def push(self, item):
        super().push(item)
        self.callBack(item)

class PushPopTimeCheckWrapper(PushPopWrapper):
    def __init__(self, dataStructure, maxTime, exception, frequency=30):
        super().__init__(dataStructure)
        self.maxTime = maxTime
        self.exception = exception
        self.frequency = frequency
        self.frequencyCounter = 0
        self.time = 0
        self.lastTime = time.process_time()

    def push(self, item):
        super().push(item)
        self._check()

    def pop(self):
        super().pop()
        self._check()

    def _check(self):
        self.frequencyCounter += 1
        if self.frequencyCounter > self.frequency:
            self.time += (time.process_time() - self.lastTime) * 1000
            if self.time > self.maxTime:
                raise self.exception


