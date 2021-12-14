infl = "in"

inp = readlines(infl)

function parsed(inp)
    dots = []
    folds = []
    X, Y = 0, 0
    for line in inp
        if startswith(line, "fold along ")
            push!(folds, split(replace(line, "fold along "=>""), "="))
        else
            x, y = parse.(Int16, split(line, ","))
            X, Y = max(X, x), max(Y, y)
            push!(dots, (x, y))
        end
    end
    dots, folds, X, Y
end

dots, folds, X, Y = parsed(inp)

function solve(dots, folds, X, Y)
    r = -1
    for (axis, n) in folds
        dots_ = Set()
        n = parse(Int16, n)
        T = reverse([0:(Dict("x"=>X, "y"=>Y)[axis] - n - 1)...])
        for (x, y) in dots
            e = axis == "x" ? x : y
            if e < n
                push!(dots_, (x, y))
            elseif  e > n
                c = axis == "x" ? (T[e-n], y) : (x, T[e-n])
                push!(dots_, c)
            end
        end
        X, Y = axis == "x" ? (X - n - 1, Y) : (X, Y - n - 1)
        dots = dots_

        if r == -1
            r = length(dots_)
        end
    end

    A = fill(" ", (Y+1, X+1))
    for (x, y) in dots
        A[y+1, x+1] = "#"
    end

    r
end

println(solve(dots, folds, X, Y))