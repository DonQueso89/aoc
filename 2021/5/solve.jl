infl = "in"
inp = map(x -> parse.(Int, split(replace(x, r"[^\d]+"=>" "))), readlines(infl))

function solve(inp)
    r::Dict{Tuple{Int, Int}, Int} = Dict()
    diag = []
    for v in inp
        u, w = v[1:2], v[3:4]
        if prod(u - w) == 0
            a, b, c, d = [u..., w...]
            for x in a:(c < a ? -1 : 1):c, y in b:(d < b ? -1 : 1):d
                r[(x, y)] = min(get(r, (x, y), -1) + 1, 1)
            end
        else
            push!(diag, v)
        end
    end
    p1 = sum(values(r))

    for v in diag
        u, w = v[1:2], v[3:4]
        d = w - u
        e = d ./ abs.(d)
        n = abs(d[1])
        for i in 0:n
            x, y = u + i * e
            r[(x, y)] = min(get(r, (x, y), -1) + 1, 1)
        end
    end
    p1, sum(values(r))
end

println(solve(inp))