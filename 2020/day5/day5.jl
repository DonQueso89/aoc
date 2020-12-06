if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input5"
end

input = readlines(infile)


function solve(s)
    arr = collect(0:127)
    a, b = s[1:7], s[8:10]
    for c in a
        l = length(arr)
        mid = Int8(ceil(l / 2))
        if c == 'F'
            arr = arr[1:mid]
        elseif c == 'B'
            arr = arr[mid + 1:l]
        end
    end
    
    row = first(arr)

    arr = collect(0:7)
    for c in b
        l = length(arr)
        mid = Int8(ceil(l / 2))
        if c == 'L'
            arr = arr[1:mid]
        elseif c == 'R'
            arr = arr[mid + 1:l]
        end
    end

    return row * 8 +  arr[1]
end

seat_ids = map(solve, input)

println("1: $(maximum(seat_ids))")

sort!(seat_ids)
l = length(seat_ids)
for a = 1: (l - 1)
    if seat_ids[a+1] - seat_ids[a] == 2
        println("2: $(seat_ids[a]+1)")
    end
end

