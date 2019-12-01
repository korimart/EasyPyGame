import multiprocessing

def sendNumbers(queue1, queue2):
    for i in range(100000):
        queue1.put(i)
        queue2.get(block=True)

if __name__ == "__main__":
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    process = multiprocessing.Process(target=sendNumbers, args=(queue2, queue1))
    process.start()

    while True:
        i = queue2.get(block=True)
        queue1.put(1)
        if i > 99998:
            break
    print("done")