# coding: utf-8

import re
from pipe import Pipe
from os.path import normcase, normpath
import pprint

class PdbDebug(object):

    RE_BREAKPOINT = re.compile(b'\(Pdb\)\sBreakpoint\s(\d{1,})\sat\s(.*?$)')
    RE_WHERE = re.compile(b'[\s|>]\s(.*?)\((\d{1,})\)<module')
    STEP_CMD = (b'c\n', b'n\n', b's\n')

    def __init__(self, file):
        self._breakpoints = []
        self._pipe = Pipe(['python3', '-m', 'pdb', file])
        # clean when process startup
        self._pipe.output()

    def _check_point(self, bp):
        if bp in self._breakpoints:
            idx = self._breakpoints.index(bp)
            self._pipe.execute(b'clear %d\n' % (idx+1))
            self._breakpoints.pop(idx)
            return -idx

        stdout,_ = self._pipe.execute(b'b %s:%d\n' % bp)
        if stdout[0] != b'(Pdb) *** Blank or comment':
            r = self.RE_BREAKPOINT.search(stdout[0])
            if r is not None:
                self._breakpoints.append(bp)
                return bp[1]
        return 0

    def breakpoint(self, file, line):
        bp = (normcase(normpath(file)).encode('utf-8'), line)
        line = self._check_point(bp)
        return bp if line > 0 else (file, line)

    def _trackback(self, stdout, stderr):
        file,line = self._parse_where(stdout[-2])
        return (file, line, stderr[-1])

    def _parse_where(self, line):
        r = self.RE_WHERE.search(line)
        return (r.group(1), r.group(2) ) if r else None

    def _where(self, stdout):
        flag,line = stdout[0],stdout[0]
        if len(stdout) >= 3:
            line = stdout[-2]

        postion = self._parse_where(line)
        if postion is None:
            stdout,_ = self._pipe.execute(b'w\n')
            # TODO: list index out of range
            postion = self._parse_where(stdout[3])

        return postion if postion else ('', -2)

    def step(self, cmd):
        '''
        param cmd 0: continue
                  1: next
                  2: step
        '''
        stdout,stderr = self._pipe.execute(self.STEP_CMD[cmd])
        if not stderr:
            return self._where(stdout)
        return self._trackback(stdout, stderr)

    def _pprint(self, var):
        stdout,_ = self._pipe.execute(b'pp %s\n' % var)
        return stdout[0].split(b'(Pdb) ')[1]

    def pprint(self, var):
        var = var.encode('utf-8')
        l = self._pprint(b"hasattr(%s, '__dict__')" % var)
        # NameError or SyntaxError
        if not l.startswith(b'*** '):
            data = self._pprint(var + b'.__dict__' if l == b'True' else var)
            type_ = self._pprint(b"type(%s)" % var)
            return b'%s %s = %s ' % (type_, var, data)
        return ''


if __name__ == "__main__":
    p = PdbDebug("E:/Downloads/1.py")
    p.breakpoint("E:/Downloads/1.py", 13)
    p.step(0)
    print(p.step(1))
    print(p.step(1))
    print(p.step(1))
    print(p.step(1))
