# coding: utf-8

import threading
import subprocess
import queue as Queue

class Pipe(object):
    
    def __init__(self, args):
        self._stdout_queue = Queue.Queue()
        self._stderr_queue = Queue.Queue()

        self._process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                         stdin=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True)

        stdout_thread = threading.Thread(target=self._write, 
                                         args=(self._process.stdout, self._stdout_queue))
        stderr_thread = threading.Thread(target=self._write, 
                                         args=(self._process.stderr, self._stderr_queue))

        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()

    def _write(self, fd, queue):
        ''' read pipe to queue '''
        try:
            for line in iter(fd.readline, b""):
                queue.put(line)
        finally:
            queue.put(None)

    def _readlines(self, queue, flag=False):
        lines = []
        while True:
            try:
                line = queue.get(True, 0.1)
                if line is None: break
                lines.append(line.rstrip(b"\r\n"))
            except Queue.Empty:
                if flag or lines: break
        return lines

    def execute(self, cmd : bytes) -> tuple:
        self._process.stdin.write(cmd)
        self._process.stdin.flush()
        return self.output()

    def output(self):
        return (self._readlines(self._stdout_queue), 
                self._readlines(self._stderr_queue, True))

if __name__ == "__main__":
    import time
    Pipe(['python3', '-m', 'pdb', 'E:/Downloads/1.py'])
