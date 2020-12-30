if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))

p1, p2 = [], []
c = p1
for line in inp
    if line == "Player 2:"
        global c = p2
    elseif length(line) > 0 && isdigit(line[1])
        push!(c, parse(Int, line))
    end
end

_p1, _p2 = [p1...], [p2...]

while length(p1) > 0 && length(p2) > 0
    e1, e2 = popat!(p1, 1), popat!(p2, 1)
    if e1 > e2
        push!(p1, e1, e2)
    elseif e2 > e1
        push!(p2, e2, e1)
    end
end

winner = length(p1) > 0 ? p1 : p2
println("1: $(sum(winner .* [i for i = length(winner):-1:1]))")

function play(p1::Array{Int}, p2::Array{Int}):: Int
    arch = Set()
    while length(p1) > 0 && length(p2) > 0
        if [1, p1..., 2, p2...] in arch
            return 1
        end
        push!(arch, [1, p1..., 2, p2...])

        e1, e2 = popat!(p1, 1), popat!(p2, 1)
        if length(p1) >= e1 && length(p2) >= e2
            winner = play([p1[1:e1]...], [p2[1:e2]...])
            if winner == 1
                push!(p1, e1, e2)
            else
                push!(p2, e2, e1)
            end
        else
            if e1 > e2
                push!(p1, e1, e2)
            elseif e2 > e1
                push!(p2, e2, e1)
            end
        end
    end

    return length(p1) > 0 ? 1 : 2
end

play(_p1, _p2)
println(_p2)

winner = length(_p1) > 0 ? _p1 : _p2
println("2: $(sum(winner .* [i for i = length(winner):-1:1]))")