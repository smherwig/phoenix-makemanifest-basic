#!/usr/bin/env lua5.3

-- simplified version of echo(1)

local io = require 'io'
local os = require 'os'

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

local nargs = #arg
for i, v in ipairs(arg) do
    printf("%s", v)
    if i ~= nargs then
        printf(" ")
    end
end
printf("\n")

os.exit(0)
