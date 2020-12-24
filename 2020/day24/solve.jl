if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

iset = readlines(open(fname))

parser = r"e|w|nw|ne|sw|se"

e = [2, 0]
w = [-2, 0]
se = [1, 2]
sw = [-1, 2]
ne = [1, -2]
nw = [-1, -2]

tiles = Dict{Vector{Int}, Bool}()
adj(c::Vector{Int}) = [c+x for x in [e, w , se, sw, nw, ne]]

for i in iset
    k = mapreduce(x -> eval(Symbol(x.match)), +, [x for x in eachmatch(parser, i)], init=[0, 0])
    tiles[k] = !get(tiles, k, false)
end

println("1: $(sum(values(tiles)))")

for i=1:100
    newgen = Dict{Array{Int}, Bool}()
    newnodes = Set()
    for (t, s) in tiles
        ns = 0
        for n in adj(t)
            ns += get(tiles, n, false)
            if !haskey(tiles, n)
                push!(newnodes, n)
            end
        end
        if (s && (ns == 0 || ns > 2)) || (!s && ns == 2)
            newgen[t] = !s
        else 
            newgen[t] = s
        end
    end

    for t in newnodes
        ns = sum(get(tiles, n, false) for n in adj(t))
        newgen[t] = ns == 2 ? true : false
    end
    global tiles = newgen
end

println("2: $(sum(values(tiles)))")
