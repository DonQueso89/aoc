infl = "in"
fd = split(replace(read(infl, String), " 0" => " 111 "), '\n')
chosen = parse.(Int8, split(fd[1], ','))

n = 5

function solve(boards, chosen)
    v = ones(n, 1)
    won = []
    correct = true
    corrected = [i for i in 1:length(boards) if 111 in boards[i]]
    for c in chosen
        if c == 0
            c = 111
            correct = false
        end
        for i in 1:length(boards)
            R = boards[i]
            if isnothing(R)
                continue
            end
            R = (x->x == c ? 0 : x).(R)
            if 0 in R * v || 0 in transpose(R) * v
                correction = (correct && i in corrected) ? 111 : 0
                push!(won, (sum(R)-correction) * c)
                boards[i] = nothing
                if length(won) == length(boards)
                    return won[1], won[end]
                end
            else
                boards[i] = R
            end
        end
    end
end

function boards(inp)
    r = []
    while length(inp) > 1
        m = zeros(Int8, n, n)
        for y in 1:n
            m[y, :] = parse.(Int8, split(popfirst!(inp)))
        end
        if length(inp) > 0
            popfirst!(inp)
        end
        push!(r, m)
    end
    r
end

b = boards(fd[3:end])

println(solve(b, chosen))