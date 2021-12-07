infl = "in"

inp = parse.(Int, split(read(open(infl), String), ','))

function lineage(n, t)
    r = 1
    while t - n > 0
        r += lineage(9, t - n)
        t -= 7
    end
    r
end


function solve(inp, t)
    sum([lineage(x, t) for x in inp])
end

println(solve(inp, 80))
println(solve(inp, 180))