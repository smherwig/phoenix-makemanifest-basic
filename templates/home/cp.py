import sys

BLOCK_SIZE = 4096

src = sys.argv[1]
dst = sys.argv[2]

fsrc = open(src)
fdst = open(dst, 'w')


block = fsrc.read(BLOCK_SIZE)
while block:
    fdst.write(block)
    block = fsrc.read(BLOCK_SIZE)

fsrc.close()
fdst.close()
