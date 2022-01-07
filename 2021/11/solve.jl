import Base.Iterators.product
infl = "in"

inp = map(r -> [parse.(Int8, c) for c in r], readlines(infl))

A = collect(transpose(hcat(inp...)))

function adjacent(y, x, Y, X)
    a = []
    for d in [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
        dy, dx = [y, x] + d
        if 1 <= dx <= X && 1 <= dy <= Y
            push!(a, (dy, dx))
        end
    end
    return a
end

function solve(A::Matrix{Int8})
    steps = 1
    Y, X = size(A)
    r = 0
    r2 = -1
    while r2 == -1
        work = [product(1:Y, 1:X)...]
        while length(work) > 0
            y, x = pop!(work)
            if A[y, x] < 10
                A[y, x] += 1
                if A[y, x] == 10
                    r += 1 * (steps <= 100)
                    push!(work, adjacent(y, x, Y, X)...)
                end
            end
        end

        A[A.==10] .= 0
        if sum(A) == 0
            r2 = steps
        end
        steps += 1
    end
    r, r2
end


println(solve(A))