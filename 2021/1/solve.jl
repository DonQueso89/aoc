inp = parse.(Int, readlines("in"))

function solve(inp, w)
    r = 0
    for i in w+1:length(inp)
        d = sum(inp[i-w+1:i]) - sum(inp[i-w:i-1])
        if d != 0
            r += (d + abs(d))/2d
        end
    end
    r
end

println(solve(inp, 1))
println(solve(inp, 3))

