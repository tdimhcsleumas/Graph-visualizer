from threading import Thread, Semaphore
from collections import deque
import time


class Queue:
    def __init__(self):
        self.queue = deque()
        self.lock = Semaphore(1)

    def get(self):
        self.lock.acquire()
        item = self.queue.popleft() if self.queue else None
        self.lock.release()
        return item

    def put(self, item):
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()


class TaskQueue:
    def __init__(self, num_workers=1):
        self.queue = Queue()
        self.running = True
        self.workers = [
            Thread(target=self.worker, daemon=True) for _ in range(num_workers)
        ]
        for worker in self.workers:
            worker.start()

    def worker(self):
        while self.running:
            job = self.queue.get()
            if job:
                item, args, kwargs = job
                item(*args, **kwargs)

    def add_task(self, task, *args, **kwargs):
        self.queue.put((task, args, kwargs))

    def join(self):
        self.running = False
        for worker in self.workers:
            worker.join()


def tests():
    def blokkah(*args, **kwargs):
        time.sleep(5)
        print("Blokkah mofo!")

    q = TaskQueue(num_workers=5)

    for item in range(10):
        q.add_task(blokkah)

    q.join()  # block until all tasks are done

    print("All done!")


if __name__ == "__main__":
    tests()
