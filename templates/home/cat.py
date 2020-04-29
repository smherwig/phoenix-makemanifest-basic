import sys

path = sys.argv[1]
f = open(path)
for line in f:
    print(line, end='')
f.close()
