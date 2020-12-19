if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))
rules = Dict()
messages = []

for line in inp
    if startswith(line, "a") || startswith(line, "b")
        push!(messages, line)
    elseif occursin(":", line)
        k, v = split(line, ": ")
        if v in ("\"a\"", "\"b\"")
            rules[parse(Int16, k)] = v[2]
        else
            conds = map(x -> map(y -> parse(Int16, y) ,split(x)) ,split(v, " | "))
            rules[parse(Int16, k)] = conds
        end
    end
end

max_length = maximum(length, messages)

function lookup(n:: Int16, depth=1)
    conds_or_scalar = rules[n]
    memo = Dict{Int, Any}()
    if conds_or_scalar in ('a', 'b')
        return [conds_or_scalar]
    end

    alternatives = []

    for cond in conds_or_scalar
        alts = []
        alts = [get!(function() lookup(number, depth+1) end, memo, number) for number in cond]
        push!(alternatives, filter(x -> length(x) <= max_length, map(join, Iterators.product(alts...)))...)
    end

    return alternatives

end
@time println("1: $(length(intersect(lookup(Int16(0)), messages)))")