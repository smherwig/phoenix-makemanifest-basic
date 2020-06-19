#!/usr/bin/env lua5.3

local io = require 'io'
local os = require 'os'

local stdlib = require 'posix.stdlib'

local USAGE = [[
usage: printenv [VAR]

Print value of environment variable VAR.  If VAR
is not specified, print values of all environment
variables.
]]

local function die(fmt, ...)
    io.stderr:write(fmt:format(...))
    os.exit(1)
end

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

if #arg > 2 then
    die(USAGE)
end

if #arg == 1 then
    local name = arg[1]
    ret  = stdlib.getenv(name)
    print(ret)
else
    for name, value in pairs(stdlib.getenv()) do
        printf("%s=%s\n", name, value)
    end
end

os.exit(0)
