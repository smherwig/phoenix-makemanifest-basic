#!/usr/bin/env lua5.3

local os = require 'os'
local stdio = require 'posix.stdio'


local USAGE = [[
usage: rename.lua OLDPATH NEWPATH
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 2 then
    die(USAGE)
end

local oldpath = arg[1]
local newpath = arg[2]

local ret, errmsg, errnum = stdio.rename(oldpath, newpath)

if not ret then
    die('rename("%s", "%s") failed: [errno=%d]: %s\n', 
            oldpath, newpath, errnum, errmsg)
end

os.exit(0)
