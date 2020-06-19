#!/usr/bin/env lua5.3

local os = require 'os'

local dirent = require 'posix.dirent'

local USAGE = [[
usage: scandir.lua DIRPATH
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

if #arg ~= 1 then
    die(USAGE)
end

local dirpath = arg[1]
local ok, files = pcall(dirent.dir, dirpath)
if not ok then
    die("%s: %s\n", dirpath, files)
end

for _, f in ipairs(files) do
    if f ~= '.' and f ~= '..' then
        print(f)
    end
end

os.exit(0)
