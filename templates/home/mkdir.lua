#!/usr/bin/env lua5.3

local os = require 'os'
local sys_stat = require 'posix.sys_stat'

local USAGE = [[
usage: mkdir.lua PATH
]]

local function warn(fmt, ...)
    io.stderr:write(fmt:format(...))
end

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 1 then
    die(USAGE)
end

local path = arg[1]
local ret, errmsg, errnum = sys_stat.mkdir(path)
if not ret then
    warn('mkdir("%s") failed: [errno=%d]: %s\n',
            path, errnum, errmsg)
    os.exit(1)
else
    os.exit(0)
end
