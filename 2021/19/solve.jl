infl = "in"
inp = readlines(infl)

Troll = [1 0 0; 0 0 1; 0 -1 0]
Tturn = [0 -1 0; 1 0 0; 0 0 1]

rel_beacons = Dict(0=>[])

s = -1
for line in inp
    if startswith(line, "---")
        global s += 1
        rel_beacons[s] = []
        continue
    end

    if length(line) <= 1
        continue
    end

    push!(rel_beacons[s], eval(Meta.parse(string("[", line, "]"))))
end

function orientations(A)
    r = []
    for _ in 1:2
        for i in 1:3
            A = Troll*A
            push!(r, A)
            for j in 1:3
                A = Tturn*A
                push!(r, A)
            end
        end
        A = Troll*Tturn*Troll*A
    end
    r
end

function find_overlapping(rel_beacons, S0)
    for k in keys(rel_beacons)
        A = hcat(rel_beacons[k]...)
        for O in orientations(A)
            delta_count = Dict()
            for u in [S0[:, i] for i in 1:size(S0)[2]]
                for w in [O[:, j] for j in 1:size(O)[2]]
                    v = u - w
                    delta_count[v] = get(delta_count, v, 0) + 1
                end
            end
            
            for k_ in keys(delta_count)
                if delta_count[k_] >= 12
                    return k, k_, O
                end
            end
        end
    end

    nothing, nothing, nothing
end


function solve(rel_beacons)
    determined = Set()
    scanner_positions = Dict(0=>[0, 0, 0])

    s0 = pop!(rel_beacons, 0)
    push!(determined, s0...)
    S0 = hcat(s0...)
    tdist = [0, 0, 0]
    s0 = 0
    oriented = Dict(0=>S0)

    while length(rel_beacons) > 0
        n, dist, S0 = find_overlapping(rel_beacons, S0)
        if isnothing(n)
            s0 += 1 
            while s0 ∉ keys(oriented)
                s0 += 1
                s0 %= maximum(keys(oriented)) 
            end
            S0 = oriented[s0]
            continue
        end
        oriented[n] = S0
        tdist = scanner_positions[s0] + dist
        scanner_positions[n] = tdist
        pop!(rel_beacons, n) 
        push!(determined, [S0[:, i] + tdist for i in 1:size(S0)[2]]...)
        s0 = n
    end

    maxd = -Inf
    for k in keys(scanner_positions)
        for k_ in keys(scanner_positions)
            if k != k_
                maxd = max(sum(abs.(scanner_positions[k] - scanner_positions[k_])), maxd)

            end
        end
    end


    length(determined), maxd
end

println(solve(rel_beacons))