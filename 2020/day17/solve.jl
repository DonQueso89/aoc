if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))

function step(G, c)
    e = G[c...]
    sn = sum(G[map(x -> x-1:x+1, c)...]) - e
    e ? sn in (2, 3) ? true : false : sn == 3 ? true : false
end

function solve(ndims)
    D = length(inp)+4
    Gprev = falses([D for _=1:ndims]...)
    for y=1:D-4, x=1:D-4 inp[y][x] == '#' ? Gprev[x+2, y+2, [3 for i=1:ndims>>1]...] = true : nothing end
    for i = 1:6
        D += 2
        Gnext = falses(fill(D, (1, ndims))...)

        for c in Iterators.product(fill(3:D-2, (1, ndims))...)
            c = [c...]
            Gnext[c...] = step(Gprev, c .- 1)
        end

        Gprev = Gnext

    end
    return Gprev
end

println("1: $(sum(solve(3)))")
println("2: $(sum(solve(4)))")