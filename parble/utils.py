import itertools
import sys
import threading


class Spinner:
    """
    Animated spinner outputting on a stream, by default stdout.

    By default, only enabled of the stream is a tty, or if force is true
    """

    def __init__(self, disabled=False, forced=False, stream=sys.stdout):
        self.cycle = itertools.cycle(["-", "/", "|", "\\"])
        self.disabled = disabled
        self.forced = forced
        self._stream = stream
        self._stop = None
        self._thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disabled:
            return False
        self.stop()
        return False

    def start(self):
        if self.disabled:
            return
        if self._stream.isatty() or self.forced:
            self._stop = threading.Event()
            self._thread = threading.Thread(target=self.spin)
            self._thread.start()

    def stop(self):
        if not self._thread:
            return
        self._stop.set()
        self._thread.join()

    def spin(self):
        while not self._stop.is_set():
            self._stream.write(next(self.cycle))
            self._stream.flush()
            self._stop.wait(0.25)
            self._stream.write("\b")

        self._stream.write(" ")
        self._stream.write("\b")
        self._stream.flush()
