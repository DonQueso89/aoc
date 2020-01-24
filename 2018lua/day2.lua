num_two = 0
num_three = 0


function default_table ()
    -- defaultdict(int) emulation
    table = {}
    metatable = {}
    metatable["__index"] = function () return 0 end
    setmetatable(table, metatable)
    return table
end


function diff_by_one (a, b)
    n = a:len()
    i = 1
    num_diff = 0
    while i <= n
    do
        if a:byte(i) - b:byte(i) ~= 0
        then
            num_diff = num_diff + 1
        end
        if num_diff > 1
        then
            return false
        end
        i = i + 1
    end
    return num_diff == 1
end


lines = {}
x = 0
for line in io.lines("input2")
do
    counts = default_table()
    n = line:len()
    i = n
    while i > 0
    do
        ord = line:byte(i)
        counts[ord] = counts[ord] + 1
        i = i - 1
    end
    
    done = 0
    while n > 0
    do
        ord = line:byte(n)
        if done == 3 then break end
        if done & 1 == 0 and counts[ord] == 2
        then
            num_two = num_two + 1
            done = done | 1
        end
        if done & 2 == 0 and counts[ord] == 3
        then
            num_three = num_three + 1
            done = done | 2
        end
        n = n - 1
    end
    lines[x] = line
    x = x + 1
end
print(num_two * num_three)
for i=0, x-1
do
    for j=i, x-1
    do
        if diff_by_one(lines[i], lines[j])
        then
            a = lines[i] 
            b = lines[j]
            print(a)
            print(b)
            r = ""
            for z=1, a:len() do if a:byte(z) - b:byte(z) == 0 then r = r .. string.char(a:byte(z)) else r = r .. " " end end
            print(r)
        end
    end
end
