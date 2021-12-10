infl = "in"

inp = readlines(infl)

OPEN = [40, 60, 91, 123]
CLOSE = [41, 62, 93, 125]
M = Dict([c=>o for (c, o) in zip(CLOSE, OPEN)])
RM = Dict([o=>c for (c, o) in zip(CLOSE, OPEN)])

S = Dict(41=>3, 93=>57, 125=>1197, 62=>25137)
S2 = Dict(41=>1, 93=>2, 125=>3, 62=>4)

function solve(inp)
    r = 0
    incomplete = []
    for line in inp
        stack = []
        push!(incomplete, stack)
        for c in strip(line)
            c = Int(c)
            if c in OPEN
                push!(stack, c)
            else
                if M[c] == pop!(stack)
                    continue
                else
                    r += S[c]
                    pop!(incomplete)
                    break
                end
            end
        end
    end

    scores = []
    for stack in incomplete
        s = 0
        while length(stack) > 0
            s *= 5
            s += S2[RM[pop!(stack)]]
        end
        push!(scores, s)
    end

    r, sort(scores)[(length(scores) + 1) ÷ 2]
end

println(solve(inp))
