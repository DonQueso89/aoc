if length(ARGS) > 0
    infile = ARGS[1]
    npreamb = parse(Int8, ARGS[2])
else
    infile = "input9"
    npreamb = 25
end

prep(x) = parse(Int64, x)
input = map(prep, readlines(infile))

function solve(xmas, n)
    cache = xmas[1:n]
    for i = n+1:length(xmas)
        e = xmas[i]
        test = filter(x -> x < e, cache)
        valid = any([e - x in test for x in test])
        if !valid
            return e
        end
        popfirst!(cache)
        push!(cache, e)
    end
end

ans = solve(input, npreamb)
println("1: $ans")

for j = 1:20, i = 1:length(input)-j
    r = input[i:i+j]
    if sum(r) == ans
        println("2: $(maximum(r) + minimum(r))")
    end
end