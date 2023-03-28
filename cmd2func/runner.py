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
        self.proc: T.Optional[subp.Popen] = None
        self.t_stdout: T.Optional[Thread] = None
        self.t_stderr: T.Optional[Thread] = None

    def run(self, **kwargs: T.Any):
        """Run the command using subprocess.Popen.

        Args:
            **kwargs: keyword arguments for subprocess.Popen
        """
        exe = shlex.split(self.command)
        self.proc = subp.Popen(
            exe, stdout=subp.PIPE, stderr=subp.PIPE, **kwargs)
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

    def write_stream_until_stop(
            self,
            out_file: T.TextIO,
            err_file: T.TextIO) -> int:
        g = self.stream()
        retcode = None
        while True:
            try:
                src, line = next(g)
                if src == 'stdout':
                    out_file.write(line)
                else:
                    err_file.write(line)
            except StopIteration as e:
                retcode = e.value
                break
        return retcode
