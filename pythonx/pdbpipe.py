# coding: utf-8

import os
import re
import subprocess
import threading
import queue as Queue

class Pdbpipe(object):

    RE_BREAKPOINT = re.compile('\(Pdb\)\sBreakpoint\s(\d{1,})\sat\s(.*?$)')
    RE_NEXT = re.compile('[>|\s]\s*([^\(].+)\((\d{1,})\)')
    
    def __init__(self, file):
        self._breakpoints = []
        self._queue = Queue.Queue()
        self._process = subprocess.Popen(['python3', '-m', 'pdb', file],
                                         stdout=subprocess.PIPE,
                                         stdin=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         shell=True)

        stdout_thread = threading.Thread(target=self._readThread,
                                         args=(self._process.stdout, self._queue))
        stdout_thread.daemon = True
        stdout_thread.start()
        self._readQueue()

    def execute(self, cmd):
        self._process.stdin.write(cmd)
        self._process.stdin.flush()
        return self._readQueue()

    def _readQueue(self):
        output = []
        while True:
            try:
                line = self._queue.get(True, 0.1)
                if line is None: break
                output.append(line.rstrip(b"\r\n"))
            except Queue.Empty:
                if output: break
        return output

    def _readThread(self, fd, queue):
        try:
            for line in iter(fd.readline, b""):
                queue.put(line)
        finally:
            queue.put(None)

    def _parseWhere(self):
        output = self.execute(b'w\n')
        if output[-1].startswith(b'> <frozen'):
            r = self.RE_NEXT.search(output[-3].decode('utf-8'))
        else:
            r = self.RE_NEXT.search(output[-2].decode('utf-8'))
        if not r: return ('', 0)
        return (r.group(1), r.group(2))

    def breakpoint(self, file, line):
        bp = (os.path.normcase(os.path.normpath(file)), line)
        for i, param in enumerate(self._breakpoints):
            if bp == param:
                self.execute(('clear {}\n'.format(i+1)).encode('utf-8'))
                del self._breakpoints[i]
                return ('', -1)

        output = self.execute(('b {}:{}\n'.format(file, line)).encode('utf-8'))[0]
        if output != b'(Pdb) *** Blank or comment':
            r = self.RE_BREAKPOINT.search(output.decode('utf-8'))
            if r is not None:
                self._breakpoints.append(bp)
                return bp
        return ('', 0)
        
    def next(self):
        self.execute(b'n\n')
        return self._parseWhere()

    def continues(self):
        self.execute(b'c\n')
        return self._parseWhere()

    def step(self):
        self.execute(b's\n')
        return self._parseWhere()

    def print(self, var):
        output = self.execute(b'pp %s\n' % var)[0]
        return output.decode('utf-8').split('(Pdb) ')[1]


if __name__ == "__main__":
    import pprint
    p = Pdbpipe('E:/Downloads/1.py')
    print(p.breakpoint('E:/Downloads/1.py', 9))
    print(p.breakpoint('E:/Downloads/1.py', 9))
