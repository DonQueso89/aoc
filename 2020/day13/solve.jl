if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

iset = readlines(open(fname))


function nextbus(target, ids)
    return reduce(*, sort(collect(zip(ids, map(x -> ((target÷x) + 1) * x - target, ids))), by=x -> x[2])[1])
end

target, ids = parse(Int32, iset[1]), map(x -> parse(Int16, x), split(replace(iset[2], r"x,"=>""), ","))
println("1: $(nextbus(target, ids))")


function nextcontiguous()
    """
    Specific fast solution for my input

    (1, 19)
    (10, 41)
    (20, 859)
    (28, 23)
    (33, 13)
    (37, 17)
    (49, 29)
    (51, 373)
    (88, 37)

    pos 20 = multiple of 19,859,13,17 and 29
    pos 51 = multiple of 373,41,23 and 37
    """
    p1 = reduce(*, [19,859,13,17,29])
    p2 = reduce(*, [373,41,23,37])
    k = 1

    while true
        e = p1 * k
        if (e + 31) % p2 == 0
            # => 905694340256752
            return e-19
        end
        k += 1
    end
end

function nextcontiguous(buses::Array{SubString{String}, 1})
    """Generalized solution which is slower because it runs a divisibility test
    on the whole probe vector"""
    l = length(buses)
    div_test_vector = [parse(Int, replace(x, r"x"=>"1")) for x in buses]
    product_per_idx = [i=>reduce(*, [[y for (j, y) in enumerate(div_test_vector) if y > 1 && abs(i-j)==y]..., div_test_vector[i]]) for i in 1:l]
    probe = sort(product_per_idx, by=x -> x.second)[end]
    attempt = 0
    while true
        attempt += probe.second
        sequence = collect((attempt - probe.first + 1):(attempt + (l-probe.first)))
        if any(x > 0 for x in sequence .% div_test_vector)
            continue
        end
        return attempt - probe.first + 1
    end    
end

println("2 fast and specific: $(nextcontiguous())")
println("2 slow and generic: $(nextcontiguous(split(iset[2], ",")))")