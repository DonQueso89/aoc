if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

ticket = readlines(open(fname))

prep(a) = map(x -> parse(Int, x), a)

tickets = []
ranges = []
for i = 1:length(ticket)
    e = ticket[i]
    if startswith(e, "your")
        push!(tickets, split(ticket[i+1], ",") |> prep)
    elseif startswith(e, "nearby")
        push!(tickets, map(x -> split(x, ",") |> prep, ticket[i+1:end])...)
    elseif occursin("-", e)
        push!(ranges, split(split(e, ": ")[2], " or ")...)
    end
end
ranges = map(r -> map(x -> parse(Int, x), split(r, "-")), ranges)
_ranges = [[ranges[i]..., ranges[i+1]...] for i = 1:2:length(ranges)-1]

valid(n) = any([lobo <= n <= upbo for (lobo, upbo) in ranges])
function f()
    invalid = 0
    invalid_indices = []
    for i = 2:length(tickets)
        t = tickets[i]
        _invalid = [x for x in t if !valid(x)]
        if length(_invalid) > 0
            invalid += sum(_invalid)
            push!(invalid_indices, i)
        end
    end
    return invalid, hcat([x for (i, x) in enumerate(tickets) if !(i in invalid_indices)]...)
end

n_inv, valid_tickets = f() # valid tickets is transposed
println("1: $n_inv")

position_per_field = Dict()
n_positions, n_tickets = size(valid_tickets)

while length(position_per_field) < n_positions
    options_per_field = Dict(fid=>[] for fid = 1:n_positions)
    for p = 1:n_positions
        position_vector = valid_tickets[p, 2:n_tickets]
        
        for (field_idx, (a,b,c,d)) in enumerate(_ranges)
            if all([a <= x <= b || c <= x <= d for x in position_vector])
                push!(options_per_field[field_idx], p)
            end
        end
    end
    for (fid, pids) in options_per_field
        if length(pids) == 1
            position_per_field[fid] = first(pids)
            valid_tickets[first(pids), :] .= -1
        end
    end
end
println("2: $(reduce(*, [tickets[1][position_per_field[x]] for x = 1:6]))")