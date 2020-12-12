if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

iset = readlines(open(fname))

EAST = 0
SOUTH = 90
WEST = 180
NORTH = 270

N(x, y, n, d) = (x, y + n, d)
S(x, y, n, d) = (x, y - n, d)
E(x, y, n, d) = (x + n, y, d)
W(x, y, n, d) = (x - n, y, d)
R(x, y, n, d) = (x, y, (d + n) % 360)
L(x, y, n, d) = (x, y, (d - n) < 0 ? 360 + (d - n) : d - n)
F(x, y, n, d) = d === EAST ? E(x, y, n, d) : d === WEST ? W(x, y, n, d) : d === SOUTH ? S(x, y, n, d) : N(x, y, n, d)

function F(x, y, n, waypoint:: Tuple{Int64, Int64})
    wx, wy = waypoint
    dx, dy = wx - x, wy - y
    x, y = x + n * dx, y + n * dy
    return (x, y, (x + dx, y + dy))
end

function R(x, y, n, waypoint::Tuple{Int64, Int64})
    wx, wy = waypoint
    dx, dy = wx - x, wy - y

    for _ in 1:Int(n/90)
        dx, dy = dy, dx * -1
    end
    
    return (x, y, (x + dx, y + dy))
end
function L(x, y, n, waypoint::Tuple{Int64, Int64})
    wx, wy = waypoint
    dx, dy = wx-x, wy-y
    for _ in 1:Int(n/90)
        dx, dy = dy * -1, dx
    end
    
    return (x, y, (x + dx, y + dy))
end

function nav(iset)
    dir = EAST
    x, y = 0, 0

    for i in iset
        ins, n = i[1], parse(Int16, i[2:length(i)]) 
        x, y, dir = eval(Symbol(ins))(x, y, n, dir)
    end

    return abs(x) + abs(y)
end

function nav_by_waypoint(iset)
    wx, wy = 10, 1
    x, y = 0, 0

    for i in iset
        ins, n = i[1], parse(Int16, i[2:length(i)]) 
        if occursin(ins, "NESW")
            wx, wy, _ = eval(Symbol(ins))(wx, wy, n, 0)
        else
            x, y, waypoint = eval(Symbol(ins))(x, y, n, (wx, wy))
            wx, wy = waypoint
        end
    end
    return abs(x) + abs(y)
end

println("1: $(nav(iset))")
println("2: $(nav_by_waypoint(iset))")