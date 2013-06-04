#!/usr/bin/python2

import os
import sys
import re
import functools
import errno
import subprocess
import StringIO
import struct
import hashlib
import select
import cPickle

try:
    import pexpect
except ImportError:
    pexpect=None

class Unbuffered:
    """turn off buffering"""
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)
## this breaks bpython
# sys.stdout=Unbuffered(sys.stdout)

def main():
    print 'This script implements several useful functions.'

def is_numeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def to_numeric(string):
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            return None

def abspath(*path): # variable number of arguments
    return os.path.abspath(os.path.join(sys.path[0], *path))
    # when this function is called by another script, sys.path[0] is the path to THAT script
    # os.path.abspath was intended to convert path relative to cwd. here it's used to clean up stuff like /a/bc/../def
    # os.path.join('abc/def','/usr') ==> '/usr'

def md5sum(filename, block_size=128):
    # http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python
    md5=hashlib.md5()
    with open(filename) as f:
        while True:
            data=f.read(block_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

class DotDict(dict):
    """Provide a dict object with . access to elements
    http://www.rafekettler.com/magicmethods.html
    http://stackoverflow.com/a/224876
    """
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def key_natural(key):
    """key to sort alphanumeric stuff in the way that humans expect. Adapted from http://stackoverflow.com/a/2669120"""
    def to_float(s):
        try:
            return float(s)
        except ValueError:
            return s
    return [to_float(s) for s in re.split('([0-9.]+)', key)]

def lp(filename):
    """load cPickle as return as a DotDict, if possible"""
    if os.path.isfile(filename):
        with open(filename) as f:
            data = cPickle.load(f)
    elif os.path.isfile(filename + '.pickle'):
        with open(filename + '.pickle') as f:
            data = cPickle.load(f)
    else:
        return None

    if isinstance(data, dict):
        return DotDict(data)
    else:
        return data

class memoized(object):
    """Memoizing decorator

    Usage: @memoized before functions, memomized() around lambdas
    """
    # FIXME: this does not allow kwargs. error msg "__call__() got an unexpected keyword argument ..."
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return self.func(*args)
    def __repr__(self):
        return repr(self.func)
    def __get__(self, obj, objtype):
        """support instance methods. see http://stackoverflow.com/a/3296318"""
        return functools.partial(self.__call__, obj)

def get_input(prompt, default='default', timeout=10):
    print prompt, '(timeout = %d sec, press ENTER when finish):' % timeout,
    i, o, e = select.select([sys.stdin], [], [], timeout)
    if i:
        return sys.stdin.readline().strip()
    else:
        return default

############### toooooold ######################33

# basic filesystem operations
def absPathRel2Script(path):
    # sys.path[0] gives the full path to the script, regardless of cwd.
    return os.path.join(sys.path[0], path)
def mkdir(path):
    # '-p' = no error if existing, make parent directories as needed
    # subprocess.Popen(['mkdir -p "%s"'%path], shell=True, stderr=subprocess.PIPE).wait()
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def execute(command):
    p=subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdo,stde=p.communicate()
    return stdo,stde,p.returncode

def execute_realtime(cmd):
    if pexpect==None:   # you can also try http://stackoverflow.com/questions/527197/intercepting-stdout-of-a-subprocess-while-it-is-running
                        #              and http://stackoverflow.com/questions/2804543/read-subprocess-stdout-line-by-line
                        # but since i can install pexpect to $HOME, i wouldn't bother....
        stdo,stde,code=execute(cmd)
        for line in (stdo+stde).split('\n'):
            yield line
        assert code==0
    else:
        child = pexpect.spawn(cmd)
        while True:
            try:
                child.expect('\n', timeout=None) # http://www.noah.org/wiki/pexpect#Exceptions
                yield child.before
            except pexpect.EOF:
                break
        child.close()
        assert child.exitstatus==0

def printDict(dic):
   for key in sorted(dic.keys()):
       print key,':',dic[key]

def print2str(anything): # should be obsolete.. use repr
    datastring=StringIO.StringIO()
    print >> datastring, anything
    return datastring.getvalue()[:-1] # removes the trailing \n

def unpack(format, s, index):
    "the third argument 'index' should be [int] -- to provide a call-by-reference"
    end=index[0]+struct.calcsize(format)
    result=struct.unpack(format,s[index[0]:end])
    index[0]=end
    return result

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch=_Getch()

if __name__=='__main__':
    main()

