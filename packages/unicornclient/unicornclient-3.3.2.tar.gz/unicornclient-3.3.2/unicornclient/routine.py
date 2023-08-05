import threading
import queue

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.manager = None
        self.no_wait = False
        self.is_stopping = False

    def run(self):
        while True:
            got_task = False
            data = None

            if self.no_wait:
                try:
                    data = self.queue.get_nowait()
                    got_task = True
                except queue.Empty:
                    data = None
                    got_task = False
            else:
                data = self.queue.get()
                got_task = True

            if data:
                index = 'routine_command'
                routine_command = data[index] if index in data else None

                if routine_command == 'stop':
                    self.is_stopping = True

            self.process(data)

            if got_task:
                self.queue.task_done()

            if self.is_stopping:
                break

    def process(self, data):
        pass
