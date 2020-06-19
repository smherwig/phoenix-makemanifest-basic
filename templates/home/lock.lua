#! /usr/bin/env lua5.3

local os  = require 'os'

local F = require 'posix.fcntl'
local S = require 'posix.sys.stat'
local unistd = require 'posix.unistd'


local fd = F.open(
   'file.txt',
   F.O_CREAT + F.O_WRONLY + F.O_TRUNC,
   S.S_IRUSR + S.S_IWUSR + S.S_IRGRP + S.S_IROTH
)

-- Set lock on file
local lock = {
   l_type = F.F_WRLCK;     -- Exclusive lock
   l_whence = F.SEEK_SET;  -- Relative to beginning of file
   l_start = 0;            -- Start from 1st byte
   l_len = 0;              -- Lock whole file
}

if F.fcntl(fd, F.F_SETLK, lock) == -1 then
   error('file locked by another process')
end

-- Do something with file while it's locked
unistd.write(fd, 'Lorem ipsum\n')

-- Release the lock
lock.l_type = F.F_UNLCK
F.fcntl(fd, F.F_SETLK, lock)

os.exit(0)
