import shlex
import typing as T
import subprocess as subp
from threading import Thread
from queue import Queue


class ProcessRunner(object):
    """Subprocess runner, allow stream stdout and stderr."""
    def __init__(self, command: str) -> None:
        self.command = command
        self.queue: Queue[T.Tuple[T.IO[bytes], bytes]] = Queue(0)
        self.proc = None
        self.t_stdout = None
        self.t_stderr = None

    def run(self):
        exe = shlex.split(self.command)
        self.proc = subp.Popen(exe, stdout=subp.PIPE, stderr=subp.PIPE)
        self.proc.stdout
        self.t_stdout = Thread(
            target=self.reader_func, args=(self.proc.stdout, self.queue))
        self.t_stdout.start()
        self.t_stderr = Thread(
            target=self.reader_func, args=(self.proc.stderr, self.queue))
        self.t_stderr.start()

    @staticmethod
    def reader_func(pipe: T.IO[bytes], queue: "Queue"):
        """https://stackoverflow.com/a/31867499/8500469"""
        try:
            with pipe:
                for line in iter(pipe.readline, b''):
                    queue.put((pipe, line))
        finally:
            queue.put(None)

    def stream(self):
        """https://stackoverflow.com/a/31867499/8500469"""
        for _ in range(2):
            for source, line in iter(self.queue.get, None):
                if source is self.proc.stdout:
                    src = "stdout"
                else:
                    src = "stderr"
                line_decoded = line.decode()
                yield src, line_decoded
        return self.proc.wait()
