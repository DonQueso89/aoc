if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

EMPTY = 'L'
OCC = '#'

seats = readlines(open(fname))

M0 = [seats[i][j] == EMPTY ? 0 : -1 for i = 1:length(seats), j = 1:length(seats[1])]
rows, cols = size(M0)

function get_viz(x, y)
    r = []
    for dx in [-1, 0, 1], dy in [-1, 0, 1]
        if (dx, dy )=== (0, 0)
            continue
        end
        cx, cy = x+dx, y+dy
        while 1 <= cx <= cols && 1 <= cy <= rows
            if M0[cy, cx] === 0
                push!(r, (cx, cy))
                break
            end
            cx += dx
            cy += dy
        end
    end
    return r
end

viz_map = Dict([((x, y), get_viz(x, y)) for x = 1:cols, y = 1:rows])
adj(x, y) = filter(z -> 1 <= z[1] <= cols && 1 <= z[2] <= rows && z != (x, y),[(x+dx, y+dy) for dx in [-1,0,1], dy in [-1,0,1]])
adj_viz(x, y) = viz_map[(x, y)]
calc(A) = sum(map(x -> max(0, x), A))


function sim_step(M, adj_fn, tolerance_lvl)
    next_gen = fill(-1, (rows, cols))
    for y = 1:rows, x=1:cols
        e = M[y,x]
        if e === -1
            continue
        end
        num_occ = sum([M[ny,nx] === -1 ? 0 : M[ny,nx] for (nx, ny) in adj_fn(x, y)])
        
        if e + num_occ === 0
            next_gen[y,x] = 1
        elseif e === 1 && num_occ >= tolerance_lvl
            next_gen[y,x] = 0
        else
            next_gen[y,x] = e
        end
    end
    return next_gen
end

pretty(A) = display(map(x -> x === 1 ? '#' : x === 0 ? 'L' : '.', A))

function sim(M, adj_fn, tolerance_lvl)
    prev_occ = calc(M)
    M = sim_step(M, adj_fn, tolerance_lvl)
    next_occ = calc(M)

    while next_occ != prev_occ
        prev_occ = next_occ
        M = sim_step(M, adj_fn, tolerance_lvl)
        next_occ = calc(M)
    end

    return next_occ
end

println("1: $(sim(M0, adj, 4))")
println("2: $(sim(M0, adj_viz, 5))")
