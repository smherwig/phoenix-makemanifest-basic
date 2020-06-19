path = arg[1]
f, estr, e = io.open(path, 'r')
if not f then
    print(estr)
    os.exit(1)
end

for line in f:lines() do
    print(line)
end

f:close()
os.exit(0)
