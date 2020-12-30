import Base.Threads

if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input"
end

prep(x) = parse(Int16, x)
prepcoll(x) = (pushfirst!(x, 0); push!(x, last(x) + 3);)

input = map(prep, readlines(infile)) |> sort! |> prepcoll 

function cnt_deltas(input)
    m1, m3 = 0, 0
    l = length(input)

    for i = 2:l
        d = input[i] - input[i-1]
        if d == 1
            m1 += 1
        elseif d == 3
            m3 += 1
        end
    end

    return m1 * m3
end

println("1: $(cnt_deltas(input))")

mutable struct Node
    n:: Int16
    w:: Int128
end

nodes = map(x -> Node(x, 1), input)
neighbour_map = Dict([(node.n, [x for x in nodes if -3 <= (x.n - node.n) < 0]) for node in nodes])
sort!(nodes, by=x -> x.n)
for node in nodes
    node.w = max(sum([x.w for x in neighbour_map[node.n]]), 1)
end
println("2: $(last(nodes).w)")