#!/usr/bin/env lua5.3


local os = require 'os'
local unistd = require 'posix.unistd'


local USAGE = [[
usage: pwd.lua
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 0 then
    die(USAGE)
end

local ret, errmsg, errnum = unistd.getcwd()

if not ret then
    die('getcwd() failed: [errno=%d]: %s\n', errnum, errmsg)
end

print(ret)
os.exit(0)
