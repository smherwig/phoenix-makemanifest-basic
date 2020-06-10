#!/usr/bin/env python3

import os

r = os.uname()
print("%s %s %s %s %s" % \
    (r.sysname, r.nodename, r.release, r.version, r.machine))
