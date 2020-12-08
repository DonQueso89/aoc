if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input8"
end

prep(x) = (x[1], parse(Int16, x[2]))
input = map(prep ∘ split, readlines(infile))


acc(p, v, i) = p + 1, v + i
jmp(p, v, i) = p + i, v
nop(p, v, _) = p + 1, v

function looporhaltval(iset)
    ptr, acc = 1, 0
    l = length(iset)
    d = falses(1, l)

    while 0 < ptr <= l && !d[ptr]
        d[ptr] = 1
        i, n = iset[ptr]
        ptr, acc = eval(Symbol(i))(ptr, acc, n)
    end

    return acc, ptr
end

# 56 nops
# 223 jmps
function find_halt(iset)
    l = length(iset)
    for idx = 1:l
        i, n = iset[idx]
        if i != "acc"
            alt_iset = [iset[1:idx-1]..., (i == "jmp" ? "nop" : "jmp", n), iset[idx+1:l]...]
            acc, ptr = looporhaltval(alt_iset)

            if ptr == l + 1
                return acc
            end
        end
    end
end

a, p = looporhaltval(input)
println("1: $a")
println("2: $(find_halt(input))")