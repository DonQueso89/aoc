r = 0
input = {}
i = 0
for line in io.lines("input1")
do
    r = r + tonumber(line)
    input[i] = tonumber(line)
    i = i + 1
end
print(r)

r = 0
n = i
i = 0
cache = {}
while (not cache[r] == true)
do
    cache[r] = true
    r = r + input[i]
    i = i + 1
    i = i % n
end
print(r)
