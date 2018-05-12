from runner import TaskRunner
import time, random

class Test(TaskRunner):

    def build_queue(self):
        for i in range(50):
            self.add_task(i)
        return

    def do_task(self, task):
        time.sleep(random.randint(0, 200)/float(1000))
        print(task)
        return


x = Test(consumer_threads=5)
print(x.run())