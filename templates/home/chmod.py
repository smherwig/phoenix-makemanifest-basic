#!/usr/bin/env python3

import os
import sys

mode = int(sys.argv[1], base=8)
path = sys.argv[2]
os.chmod(path, mode) 
