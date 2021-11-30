# possible alternative: something with subtracting consecutive geometric series
function solve(len, first, last, step)
    if len == 1
        return first
    end
    if len % 2 == 0
        return solve(len / 2, first, last-step, step*2)
    end
    return solve((len - 1) / 2, first+step*2, last, step*2)
end

n = 3012210

println(solve(n, 1, n, 1))

# start at (n - (n % 2)) / 2
# pineut pattern = skip 1, skip 0, skip 1, ....