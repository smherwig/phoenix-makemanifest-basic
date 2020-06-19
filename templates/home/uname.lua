#!/usr/bin/env lua5.3

local os = require 'os'
local sys_utsname = require 'posix.sys.utsname'


local USAGE = [[
usage: uname.lua
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 0 then
    die(USAGE)
end

local ret, errmsg, errnum = sys_utsname.uname()

if not ret then
    die('uname() failed: [errno=%d]: %s\n', errnum, errmsg)
end

print(string.format('%s %s %s %s %s', ret.sysname, ret.nodename,
        ret.release, ret.version, ret.machine))
os.exit(0)
