if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))

n_precomputed = 10
adj(x, y, z) = [[x, y, z] .+ [dx, dy, dz] for dx=-1:1, dy=-1:1, dz=-1:1 if [dx, dy, dz] != [0, 0, 0]]
adj(x, y, z, w) = [[x, y, z, w] .+ [dx, dy, dz, dw] for dx=-1:1, dy=-1:1, dz=-1:1, dw=-1:1 if [dx, dy, dz, dw] != [0, 0, 0, 0]]
neighbours_map3d = Dict([[x, y, z]=>adj(x, y, z) for x = 1:n_precomputed, y=1:n_precomputed, z=1:n_precomputed])
neighbours_map4d = Dict([[x, y, z, w]=>adj(x, y, z, w) for x = 1:n_precomputed, y=1:n_precomputed, z=1:n_precomputed, w=1:n_precomputed])
neighbours_map(x, y, z) = neighbours_map3d 
neighbours_map(x, y, z, w) = neighbours_map4d
adj(c) = (r = get(neighbours_map(c...), c, adj(c...)); neighbours_map(c...)[c] = r; return r)

function step(G, c)
    sn = sum(G[n...] for n in adj(c))
    e = G[c...]

    if e == true
        if sn in (2, 3)
            return true
        else
            return false
        end
    else
        if sn == 3
            return true
        end
        return false
    end
end
step(G) = (c) -> step(G, c)

function solve(ndims)
    D = length(inp)+4
    Gprev = falses(fill(D, (1, ndims))...)
    for (y, row) in enumerate(inp)
        for (x, e) in enumerate(row)
            if e == '#'
                Gprev[x+2, y+2, [3 for i=1:ndims>>1]...] = true
            end
        end
    end

    for i = 1:6
        D += 2
        stepfn = step(Gprev)
        Gnext = falses(fill(D, (1, ndims))...)

        for c in Iterators.product(fill(3:D-2, (1, ndims))...)
            c = [c...]
            Gnext[c...] = stepfn(c .- 1)
        end

        Gprev = Gnext

    end
    return Gprev
end


println("1: $(sum(solve(3)))")
println("2: $(sum(solve(4)))")