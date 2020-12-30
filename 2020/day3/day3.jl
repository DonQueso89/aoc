if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input3"
end

input = readlines(infile)
n, m = length(input), length(input[1])

function ride_slope(dx, dy)
    n_trees = 0
    start = dy+1
    for y = start:dy:n
        x = 1 + dx*(Int16((y-1)/dy)) % m
        n_trees += input[y][x] == '#' ? 1 : 0
    end
    return n_trees
end

apply_ride(t) = ride_slope(t[1], t[2])

println("1: $(ride_slope(3, 1))")
println("2: $(last(cumprod(map(apply_ride, [(1, 1),(3, 1),(5, 1),(7, 1),(1, 2)]))))")
