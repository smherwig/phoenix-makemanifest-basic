#!/usr/bin/env python3

import os
import stat
import sys
import time

sb = os.stat(sys.argv[1])
print("mode : %d (%s)" % (sb.st_mode, stat.filemode(sb.st_mode)))
print("ino  : %d" % sb.st_ino)
print("dev  : %d" % sb.st_dev)
print("nlink: %d" % sb.st_nlink)
print("uid  : %d" % sb.st_uid)
print("gid  : %d" % sb.st_gid)
print("size : %d" % sb.st_size)
print("atime: %d (%s UTC)" % (sb.st_atime, time.gmtime(sb.st_atime)))
print("mtime: %d (%s UTC)" % (sb.st_mtime, time.gmtime(sb.st_mtime)))
print("ctime: %d (%s UTC)" % (sb.st_mtime, time.gmtime(sb.st_ctime)))
