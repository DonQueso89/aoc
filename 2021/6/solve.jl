infl = "in"

inp = parse.(Int, split(read(open(infl), String), ','))


function lineage(n, t, cache)
    if (n, t) ∈ keys(cache)
        return cache[(n, t)]
    end
    t_ = t

    r = 1
    while t - n > 0
        r += lineage(9, t - n, cache)
        t -= 7
    end
    cache[(n, t_)] = r
    r
end


function solve(inp, t)
    cache:: Dict{Tuple{Int, Int}, Int} = Dict()
    sum([lineage(x, t, cache) for x in inp])
end

println(solve(inp, 80))
println(solve(inp, 256))