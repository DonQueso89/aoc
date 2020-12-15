inp = [11,0,1,10,5,19]
if length(ARGS) > 0
    inp = get(Dict("testinput"=>[0, 3, 6]), ARGS[1], inp)
end

function f(inp, n)
    d = Dict(x=>i for (i, x) in enumerate(inp))
    last, previdx = inp[end], d[inp[end]]
    for turn = length(inp) + 1:n
        next = d[last] - previdx
        previdx = get(d, next, turn)
        d[next] = turn
        last = next
    end
    return last
end

println("1: $(f(inp, 2020))")
println("2: $(f(inp, 30000000))")