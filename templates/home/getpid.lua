#!/usr/bin/env lua5.3

local os = require 'os'

local unistd = require 'posix.unistd'

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

local pid = unistd.getpid()
local ppid = unistd.getppid()

printf("pid=%d, ppid=%d\n", pid, ppid)

os.exit(0)
