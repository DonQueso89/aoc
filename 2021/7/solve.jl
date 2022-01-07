infl = "in"
inp = parse.(Int, split(read(open(infl), String), ','))

Ε(n) = n*(n+1)/2


function solve(inp)
    s, e = minimum(inp), maximum(inp)
    min_ = Inf
    min2_ = Inf
    for i in s:e
        min_ = min(sum(abs.(inp.-i)), min_)
        min2_ = min(sum(Ε.(abs.(inp.-i))), min2_)
    end
    min_, min2_
end


println(solve(inp))