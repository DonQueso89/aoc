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

memo = Dict{Int, Any}()
function lookup(n:: Int16, depth=1)
    conds_or_scalar = rules[n]
    if conds_or_scalar in ('a', 'b')
        return [conds_or_scalar]
    end

    alternatives = []

    for cond in conds_or_scalar
        alts = []
        alts = [get!(function() lookup(number,depth+1) end, memo, number) for number in cond]
        push!(alternatives, filter(x -> length(x) <= max_length, map(join, Iterators.product(alts...)))...)
    end
    return alternatives

end

patterns = lookup(Int16(0))
valid = intersect(patterns, messages)
println("1: $(length(valid))")

rest = setdiff(messages, patterns)
"""
8: 42 | 42 8
11: 42 31 | 42 11 31
"""
rgx1 = Regex(join(map(x -> "^"*x, memo[42]), "|"))
rgx2 = Regex(join(map(x -> "^"*x, memo[31]), "|"))

patts = Dict(42=>rgx1, 31=>rgx2)

function match_layered(s::AbstractString)
    trimmed = s
    path = []
    while length(trimmed) > 0
        if !(match(patts[42], trimmed) === nothing)
            trimmed = replace(trimmed, patts[42]=>"")
            push!(path, 42)
        elseif !(match(patts[31], trimmed) === nothing)
            trimmed = replace(trimmed, patts[31]=>"")
            push!(path, 31)
        else
            break
        end
    end

    if length(trimmed) == 0
        l = length(path)
        println(path)
    end

    return false
end

n_valid = 0
for msg in messages
    if match_layered(msg)
        global n_valid += 1
    end
end

println("2: $(n_valid + length(valid))")