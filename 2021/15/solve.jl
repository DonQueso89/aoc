import DataStructures.PriorityQueue
import DataStructures.dequeue!

infl = "in"
inp = map(r -> [parse.(Int, c) for c in r], readlines(infl))

A = collect(transpose(hcat(inp...)))
Y, X = size(A)

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

function solve(A, ty, tx)
    visited = Set()
    q::PriorityQueue{Tuple{Int, Int}, Int} = PriorityQueue()
    q[(1, 1)] = 0
    D::Dict{Tuple{Int, Int}, Int} = Dict()

    while length(q) > 0
        cur = peek(q)
        dequeue!(q)
        (y, x), d = cur.first, cur.second
        for (ny, nx) in adjacent(y, x, ty, tx)
            if (ny, nx) ∈ visited
                continue
            end

            nd = d + A[ny, nx]
            if nd < get(D, (ny, nx), Inf)
                q[(ny, nx)] = nd
                D[(ny, nx)] = nd
            end
        end
        push!(visited, (y, x))
        if (y, x) == (ty, tx)
            return d
        end
    end
    return D[(ty, tx)]
end

println(solve(A, Y, X))

A = vcat([hcat([A.+i for i in y:y+4]...) for y in 0:4]...)
A[A.>9] .%= 9

println(solve(A, 5Y, 5X))