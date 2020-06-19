#!/usr/bin/env lua5.3

local os = require 'os'
local unistd = require 'posix.unistd'

local USAGE = [[
usage: unlink.lua PATH
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 1 then
    die(USAGE)
end

local path = arg[1]

local ret, errmsg, errnum = unistd.unlink(path)
if not ret then
    die('unlinik("%s") failed: [errno=%d]: %s\n', path, errnum, errmsg)
end

os.exit(0)
