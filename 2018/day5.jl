import Base.Threads

if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input5"
end

polymer = readline(open(fname))

function react(p::Array{Char})
    l = length(p)
    # handle non overlapping in one go
    for i = 2:l-1
        if abs(p[i] - p[i-1]) == 32
            return react(p[[1:i-2...,min(i+1, l):l...]])
        end
        if abs(p[i] - p[i+1]) == 32
            return react(p[[1:i-1...,min(i+2, l):l...]])
        end
    end

    return length(p)
end
#println("1 $(react(collect(polymer)))")

result = Threads.Atomic{Int64}(1 << 62)

Threads.@threads for c = 65:90 Threads.atomic_min!(result, react(collect(replace(polymer, Regex("[$(Char(c))$(Char(c+32))]")=>"")))) end


println("2 $(result[])")