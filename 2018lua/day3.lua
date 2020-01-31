function default_table (init_factory)
    -- defaultdict(int) emulation
    table = {}
    metatable = {}
    metatable["__index"] = function () return init_factory() end
    setmetatable(table, metatable)
    return table
end


fabric = default_table(function() return 0 end)
n_two = 0

for line in io.lines("input3")
do
    iter = line:gmatch("[ ,x](%d+)")
    x = tonumber(iter())
    y = tonumber(iter())
    w = tonumber(iter())
    h = tonumber(iter())
    for i = x, x + w - 1 do
       for j = y, y + h - 1
           do
               key = tostring(i) .. "x" .. tostring(j)
               fabric[key] = fabric[key] + 1
               if (fabric[key] == 2) then n_two = n_two + 1 end
           end
    end
end


setmetatable(fabric, {})

non_overlapping = nil
for line in io.lines("input3")
do
    iter = line:gmatch("(%d+)")
    id = tonumber(iter())
    x = tonumber(iter())
    y = tonumber(iter())
    w = tonumber(iter())
    h = tonumber(iter())
    no_overlap = true
    for i = x, x + w - 1 do
       for j = y, y + h - 1
           do
               key = tostring(i) .. "x" .. tostring(j)
               no_overlap = no_overlap and (fabric[key] == 1)
           end
    end
    if (no_overlap) then non_overlapping = id; break end
end

print(n_two)
print(non_overlapping)
