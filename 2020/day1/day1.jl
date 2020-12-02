if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input1"
end

expenses = map(x -> parse(Int32, x), readlines(infile))

function solve1(arr, target)
    if length(arr) > 1
        head = arr[1]
        tail = arr[2:length(arr)]
        if target - head in tail
            return head * (target-head)
        end
        return solve1(tail, target)
    end
    return nothing
end

println(solve1(expenses, 2020))

function solve2(arr)
    for idx = 1:length(arr)
        rest = 2020 - arr[idx]
        candidates = view(arr, findall(x -> x < rest, arr))

        if length(candidates) < 2
            continue
        elseif length(candidates) == 2 && sum(candidates) == rest
            factor = candidates[1] * candidates[2]
        else
            factor = solve1(candidates, rest)
        end
        if factor != nothing
            return factor * arr[idx]
        end
    end


end

println(solve2(expenses))