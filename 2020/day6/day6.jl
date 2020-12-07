if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input6"
end

input = readlines(infile)

bintrunc(c::Char)::Int32 = 1 << Int32(c - 97)

function solve(inp)
    b_any = 0
    b_all =  (1 << 32) - 1
    t_any = 0
    t_all = 0
    for line in inp
        if length(line) == 0
            t_any += count("1", bitstring(b_any))
            t_all += count("1", bitstring(b_all))
            b_any = 0
            b_all = (1 << 32) - 1
        else
            p = 0
            for c in line
                p |= bintrunc(c)
            end
            b_any |= p
            b_all &= p
        end
    end
    return t_any + count("1", bitstring(b_any)), t_all + count("1", bitstring(b_all))
end
a, b = solve(input)
println("1: $a")
println("2: $b")