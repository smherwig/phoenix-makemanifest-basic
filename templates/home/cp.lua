BLOCK_SIZE = 4096
src = arg[1]
dst = arg[2]

fsrc, estr, e = io.open(src, 'r')
if not fsrc then
    print(estr)
    os.exit(1)
end

fdst, estr, e = io.open(dst, 'w')
if not fdst then
    print(estr)
    os.exit(1)
end

block = fsrc:read(BLOCK_SIZE)
while block do
    fdst:write(block)
    block = fsrc:read(BLOCK_SIZE)
end

fsrc:close()
fdst:close()
os.exit(0)
