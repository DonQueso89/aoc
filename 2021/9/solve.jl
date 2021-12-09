infl = "in"

inp = map(r -> [parse.(Int8, c) for c in r], readlines(infl))

A = collect(transpose(hcat(inp...)))

function adjacent(y, x, Y, X)
    a = []
    for d in [[1, 0], [0, 1], [-1, 0], [0, -1]]
        dy, dx = [y, x] + d
        if 1 <= dx <= X && 1 <= dy <= Y
            push!(a, [dy, dx])
        end
    end
    return a
end

function solve(A::Matrix{Int8})
    Y, X = size(A)
    r = 0
    low_points = []
    for y in 1:Y
        for x in 1:X
            e = A[y, x]
            score = e + 1
            for v in adjacent(y, x, Y, X)
                try
                    if e >= A[v...]
                        score = 0
                        break
                    end
                catch
                    continue
                end
            end
            if score > 0
                push!(low_points, [y, x])
            end
            r += score
        end
    end
    
    basins = []
    for lp in low_points
        visited = Set()
        explore = Set([lp])
        size_ = 1
        while length(explore) > 0
            for v in explore
                for n in adjacent(v[1], v[2], Y, X)
                    if n ∉ visited && n ∉ explore && A[n...] < 9
                        push!(explore, n)
                        size_ += 1
                    end
                end
                push!(visited, v)
            end
            setdiff!(explore, visited)
        end
        push!(basins, size_)
    end
    r, prod(sort(basins, rev=true)[1:3])
end


println(solve(A))