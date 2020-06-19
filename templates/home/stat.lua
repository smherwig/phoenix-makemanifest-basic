#!/usr/bin/env lua5.3

local io = require 'io'
local os = require 'os'
local sys_stat = require 'posix.sys.stat'

local USAGE = [[
usage: stat.lua PATH
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

if #arg ~= 1 then
    die(USAGE)
end

local path = arg[1]

local ret, errmsg, errnum = sys_stat.stat(path)
if not ret then
    die('stat("%s") failed: [errno=%d]: %s\n', path, errnum, errmsg)
end

printf("Hello, World!\n")
printf("mode : 0o%o\n", ret.st_mode)
printf("ino  : %d\n", ret.st_ino)
printf("dev  : %d\n", ret.st_dev)
printf("nlink: %d\n", ret.st_nlink)
printf("uid  : %d\n", ret.st_uid)
printf("gid  : %d\n", ret.st_gid)
printf("size : %d\n", ret.st_size)
printf("atime: %d (%s UTC)\n", ret.st_atime, os.date("!%c", ret.st_atime))
printf("mtime: %d (%s UTC)\n", ret.st_mtime, os.date("!%c", ret.st_mtime))
printf("ctime: %d (%s UTC)\n", ret.st_ctime, os.date("!%c", ret.st_ctime))

os.exit(0)
