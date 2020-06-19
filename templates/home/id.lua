#!/usr/bin/env lua5.3

-- simplified version of id(1)

local os = require 'os'

local unistd = require 'posix.unistd'

local function printf(fmt, ...)
    io.stdout:write(fmt:format(...))
end

local uid = unistd.getuid()
local gid = unistd.getgid()
local groups = unistd.getgroups()

printf('uid=%d gid=%d groups=', uid, gid)

local ngrp = #groups
for i,grp in ipairs(groups) do
    printf("%s", grp)
    if i ~= ngrp then
        printf(", ")
    end
end
printf("\n")

os.exit(0)


