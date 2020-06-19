#!/usr/bin/env lua5.3

local io = require 'io'
local os = require 'os'

local M = require 'posix.sys.socket'
local unistd = require 'posix.unistd'

local USAGE = [[
usage: wget.lua URL
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

local r, err = M.getaddrinfo('www.cs.umd.edu', 'http', 
        {family=M.AF_INET, socktype=M.SOCK_STREAM})
if not r then
    error(err)
end

for k,v in pairs(r[1]) do
    print(k,v)
end

local fd = M.socket(M.AF_INET, M.SOCK_STREAM, 0)
local ret, errmsg, errnum = M.connect(fd, r[1])

M.send(fd, 'GET /~smherwig/index.html HTTP/1.0\r\nHost: www.cs.umd.edu\r\n\r\n')
local data = {}
while true do
    local b = M.recv(fd, 1024)
    if not b or #b == 0 then
        break
    end
    io.stdout:write(b)
end

unistd.close(fd)
os.exit(0)
