#!/usr/bin/env lua5.3

local os = require 'os'
local sys_stat = require 'posix.sys.stat'

local USAGE = [[
usage: chmod.lua MODE PATH

MODE is given in octal, (e.g. 755 for rwxr-xr-x)
]]


local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 2 then
    die(USAGE)
end

local mode = tonumber(arg[1], 8)
if not mode then
    die("MODE must be a number\n")
end

local path = arg[2]

local ret, errmsg, errnum = sys_stat.chmod(path, mode)
if not ret then
    die('chmod("%s", %s) failed: [errno=%d]: %s\n',
            path, arg[2], errnum, errmsg)
end

os.exit(0)
