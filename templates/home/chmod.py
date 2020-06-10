#!/usr/bin/env python3

import os
import sys

path = sys.argv[1]
mode = int(sys.argv[2], base=8)
os.chmod(sys.argv[1], mode) 
