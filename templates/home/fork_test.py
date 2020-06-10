#!/usr/bin/env python3

import os
import sys

f = open(sys.argv[1])

print("parent pid=%d" % os.getpid())

pid = os.fork()

if pid == 0:
    for line in f:
        print("child (%d): %s" % (os.getpid(), line))
    sys.exit(5)
else:
    print("parent waiting on child %d" % pid)
    pid, status, = os.waitpid(pid, 0)
    if os.WIFEXITED(status):
        print("child exited normally with exit status=%d" % \
                os.WEXITSTATUS(status))
    elif os.WIFSIGNALED(status):
        print("child terminated by signal: %d" % \
                os.WTERMSIG(status))
    else:
        print("child terminated with unknown status (%d) from os.waitpid" % \
                status)
    f.close()
    sys.exit(1)
