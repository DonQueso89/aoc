fname = "input6"
md = 10000
if length(ARGS) > 0
    fname = ARGS[1] # testinput6
    md = parse(Int8, ARGS[2]) # 32
end

coords = map(x -> map(y -> parse(Int, y), split(x, ", ")), readlines(open(fname)))
cols, rows = maximum(coords)
oob((x, y)) = !(1 <= x <= cols && 1 <= y <= rows)

function solve()
    dp_coord = Dict(c=>[] for c in coords)
    n = 0
    for y = 0:rows+90, x = 0:cols+90
        D = sort!([[cx, cy]=>sum((abs(x - cx), abs(y - cy))) for (cx, cy) in coords], by=x -> x.second)
        if sum([p.second for p in D]) < md
            n += 1
        end
        if D[1].second == D[2].second
            continue
        end

        push!(dp_coord[D[1].first], (x, y))
    end
    candidates = [dp_coord[x] for x in keys(dp_coord) if !any(map(oob, dp_coord[x]))]
    return maximum(length, candidates), n
end
a, b = solve()
println("1: $a\n2: $b")