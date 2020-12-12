if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

iset = readlines(open(fname))

EAST, SOUTH, WEST, NORTH = 0, 90, 180, 270

move(dvector::Array{Int64}) = (pos::Array{Int64}, n::Int16, d::Int16=Int16(0)) -> (pos + dvector * n, d)
N, S, E, W = move([0, 1]), move(-[0, 1]), move([1, 0]), move(-[1, 0])
R(pos::Array{Int64}, n::Int16, d::Int16) = (pos, (d + n) % 360)
L(pos, n::Int16, d::Int16) = (pos, (d - n) < 0 ? 360 + (d - n) : d - n)
F(pos, n::Int16, d::Int16) = Dict(EAST=>E, WEST=>W, SOUTH=>S, NORTH=>N)[d](pos, n, d)
R(waypoint::Array{Int64}, n::Union{Int16, Int64})  = (r = circshift(waypoint, 1) .* [1, -1]; n == 90 ? [r, 0] : R(r, n - 90))
L(waypoint::Array{Int64}, n::Union{Int16, Int64})  = (r = circshift(waypoint, 1) .* [-1, 1]; n == 90 ? [r, 0] : L(r, n - 90))

function nav(iset)
    dir::Int16 = EAST
    pos = [0, 0]

    for i in iset
        ins, n = i[1], parse(Int16, i[2:end]) 
        pos, dir = eval(Symbol(ins))(pos, n, dir)
    end

    return sum(abs.(pos))
end

function nav_by_waypoint(iset)
    waypoint = [10, 1]
    pos = [0, 0]

    for i in iset
        ins, n = i[1], parse(Int16, i[2:end]) 
        if occursin(ins, "NESWRL")
            waypoint, _ = eval(Symbol(ins))(waypoint, n)
        else
            pos += waypoint * n
        end
    end
    return sum(abs.(pos))
end

println("1: $(nav(iset))")
println("2: $(nav_by_waypoint(iset))")