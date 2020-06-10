#!/usr/bin/env python3

import os
import sys

# rename argv[1] to argv[2]
os.rename(sys.argv[1], sys.argv[2])
