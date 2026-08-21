import sys
import queue
import threading


class LogCapture:
    """
    Redirects sys.stdout so that any print statement is captured
    and broadcasted thread-safely to connected SSE clients.
    """

    def __init__(self):
        self.original_stdout = sys.stdout
        self.queues = set()
        self.lock = threading.Lock()
        self.is_capturing = False

    def start(self):
        if not self.is_capturing:
            sys.stdout = self
            self.is_capturing = True

    def stop(self):
        if self.is_capturing:
            sys.stdout = self.original_stdout
            self.is_capturing = False

    def write(self, message):
        self.original_stdout.write(message)
        self.original_stdout.flush()

        if message:
            with self.lock:
                for q in self.queues:
                    try:
                        q.put_nowait(message)
                    except queue.Full:
                        pass

    def flush(self):
        self.original_stdout.flush()

    def register(self, q):
        with self.lock:
            self.queues.add(q)

    def unregister(self, q):
        with self.lock:
            self.queues.discard(q)


log_capture = LogCapture()
