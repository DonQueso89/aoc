if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

iset = readlines(open(fname))


function nextbus(iset)
    target, ids = parse(Int32, iset[1]), map(x -> parse(Int16, x), split(replace(iset[2], r"x,"=>""), ","))
    return reduce(*, sort(collect(zip(ids, map(x -> ((target÷x) + 1) * x - target, ids))), by=x -> x[2])[1])
end

println("1: $(nextbus(iset))")


function nextcontiguous()
    """
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
            println("2: $(e-19)")
            break
        end
        k += 1
    end
end

nextcontiguous()