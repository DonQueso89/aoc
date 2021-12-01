inp = map(x -> parse.(Int, x), split.(readlines("input20"), "-"))

sort!(inp, by=first)

function solve(inp)
    contiguous_until = 0
    n_allowed = 0
    smallest = 0
    for (s, e) in inp
        if s > contiguous_until + 1
            if smallest == 0
                smallest = contiguous_until + 1
            end
            n_allowed += s - contiguous_until - 1
            contiguous_until = e
        else
            contiguous_until = max(e, contiguous_until)
        end
    end
    smallest, n_allowed
end

println(solve(inp))