#!/usr/bin/env python3

import os
import stat
import sys

for dent in os.scandir(sys.argv[1]):
    print("{name: %s, path: %s, inode: %d}" % \
            (dent.name, dent.path, dent.inode()))
