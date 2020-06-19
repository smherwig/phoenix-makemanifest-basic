#!/usr/bin/env lua5.3

local os = require 'os'
local unistd = require 'posix.unistd'


local USAGE = [[
usage: rmdir.lua EMPTYDIR
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 1 then
    die(USAGE)
end

local emptydir = arg[1]

local ret, errmsg, errnum = unistd.rmdir(emptydir)

if not ret then
    die('rmdir("%s") failed: [errno=%d]: %s\n', emptydir, errnum, errmsg)
end

os.exit(0)
