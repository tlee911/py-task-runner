import queue, threading
import datetime

class Stats:
    d = {}

    def __repr__(self):
        return str(self.d)

    def __str__(self):
        return '\n'.join(['\t{k}: {v}'.format(k=k, v=v) for k, v in self.d.items()])

    def add(self, key):
        if self.d.get(key) is None:
            self.d[key] = 1
        else:
            self.d[key] += 1
        return

    def put(self, key, value):
        self.d[key] = value
        return

class TaskRunner:
    def __init__(self, producer_threads=1, consumer_threads=2, q_delay=-1):
        self.producer_threads = producer_threads
        self.consumer_threads = consumer_threads
        self.q = queue.Queue()
        self.q_delay = q_delay
        self.stats = Stats()

    def build_queue(self):
        raise NotImplementedError
        return

    def do_task(self, task):
        raise NotImplementedError
        return

    def add_task(self, task):
        self.q.put(task)
        return

    def consumer(self):
        while not self.q.empty():
            task = self.q.get()
            self.do_task(task)
            self.q.task_done()
        return

    def start_consumers(self):
        for i in range(self.consumer_threads):
            thread = threading.Thread(target=self.consumer)
            thread.start()
        return

    def run(self):
        self.build_queue()
        print('Queue has {size} tasks'.format(size=self.q.qsize()))
        start = datetime.datetime.now()
        self.start_consumers()
        self.q.join()
        end = datetime.datetime.now()
        duration = int(1000 * (end - start).total_seconds())
        self.stats.put('duration', '{ms}ms'.format(ms=duration))
        return self.stats