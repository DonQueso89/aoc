import Base.display


if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))
options_per_all = Dict()
counts_per_ing = Dict()
total_set = Set()

for line in inp
    data = split(rstrip(line, ')'), " (contains ")

    ing = split(data[1])
    allers = []
    if length(data) > 1
        allers = split(data[2], ", ")
    end

    for aller in allers
        options = get(options_per_all, aller, Set(ing))
        options_per_all[aller] = intersect(options, Set(ing))
    end

    push!(total_set, ing...)

    for i in ing
        cnt = get(counts_per_ing, i, 0)
        counts_per_ing[i] = cnt + 1
    end
end

total_options = Set()
for c in values(options_per_all)
    push!(total_options, c...)
end

println("1: $(sum([counts_per_ing[x] for x in  setdiff(total_set, total_options)]))")

mapped = Dict()
while length(mapped) < length(options_per_all)
    for (aller, options) in options_per_all
        candidates = intersect(total_options, options)
        if length(candidates) == 1
            mapped[aller] = pop!(candidates)
            pop!(total_options, mapped[aller])
        end
    end
end

println("2: $(join(map(x -> x.second, sort([x for x in mapped], by=x -> x[1])), ","))")