if length(ARGS) > 0
    kc, kd = 5764801, 17807724
else
    kc, kd = 8184785, 5293040
end

N = 20201227

function solve()
    e = 7^8
    lc ,ld = 8, 8

    while e != kc
        e *= 7
        e %= N
        lc += 1
    end

    e = 7^8

    while e != kd
        e *= 7
        e %= N
        ld += 1
    end

    s = e
    e = 1
    for _ = 1:lc
        e *= s
        e %= N
    end


    println("1: $e")
end

solve()