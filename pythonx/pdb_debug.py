# coding: utf-8

import re
from pipe import Pipe
from os.path import normcase, normpath
import pprint

class PdbDebug(object):

    RE_BREAKPOINT = re.compile(b'\(Pdb\)\sBreakpoint\s(\d{1,})\sat\s(.*?$)')
    RE_WHERE = re.compile(b'[>|\s]\s*([^\(].+)\((\d{1,})\)')
    STEP_TYPES = (b'c\n', b'n\n', b's\n')
    
    def __init__(self, file):
        self._breakpoints = []
        self._pipe = Pipe(['python3', '-m', 'pdb', file])
        # clean when process startup
        self._pipe.output()

    def _traceback(self, stdout, stderr):
        file,line = self._parse_where(stdout[-2])
        return (file, line, stderr[-1])

    def _parse_where(self, line : bytes):
        r = self.RE_WHERE.search(line) 
        return ('', 0) if not r else (r.group(1), r.group(2))

    def _where(self):
        ''' where command '''
        stdout,_ = self._pipe.execute(b'w\n')
        if len(stdout) > 3:
            idx = 3 if stdout[-1].startswith(b'> <frozen') else -2
            return self._parse_where(stdout[idx])
        return ('', -2)

    def step(self, idx):
        ''' idx in [ 0 : continue, 1 : next, 2 : step ] '''
        stdout,stderr = self._pipe.execute(self.STEP_TYPES[idx])
        if len(stdout) == 3:  # Error
            return self._parse_where(stdout[1]) + (stdout[0][6:],)
        elif not stderr:
            return self._where()

        return self._traceback(stdout, stderr)

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
    p.breakpoint("E:/Downloads/1.py", 2)
    p.step(0)
    print(p.step(2))
