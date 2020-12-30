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

rgx1 = Regex(join(map(x -> "^"*x, memo[42]), "|"))
rgx2 = Regex(join(map(x -> "^"*x, memo[31]), "|"))

patts = Dict(42=>rgx1, 31=>rgx2)

function lexer(s::AbstractString)
    trimmed = s
    path::Array{Int} = []
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
    return path
end

function grammar_valid(tokens::Array{Int})
    """
    8: 42 | 42 8
    11: 42 31 | 42 11 31
    """
    if length(tokens) < 3
        return false
    end

    if first(tokens) == 31 || tokens[2] == 31
        return false
    end

    if all(tokens .== 42) || all(tokens .== 31)
        return false
    end

    if tokens[end] == 42
        return false
    end

    n_42_required = 0
    while tokens[end] == 31
        n_42_required += 1
        pop!(tokens)
    end

    if length(tokens) >= n_42_required + 1 && all(tokens .== 42)
        return true
    end

    return false
end

n_valid = 0
for msg in messages
    tokens = lexer(msg)
    if grammar_valid(tokens)
        global n_valid += 1
    end
end
println(patts[42])
println(patts[31])
println("2: $n_valid")