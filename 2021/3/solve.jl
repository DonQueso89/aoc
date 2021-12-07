# TODO: utils
import Base.+

+(a::String, b::String) = string(a, b)

inf = "in"
n = length(readline(inf))
inp = readlines(inf)
binp = map(x-> [parse.(Int16, [x...])...], readlines(inf))

agg(v) = v .+ -1

function most_common(inp)
    t = length(inp) / 2 * -1
    n = length(inp[1])
    ϵ = map(y-> y > t || y == t, reduce((a,e)->a+e.+-1, inp, init=zeros(n)))
    γ = parse(Int, sum(string.(Int.(map(!, ϵ)))), base=2)
    ϵ = parse(Int, sum(string.(Int.(ϵ))), base=2)
    ϵ, γ
end
ϵ, γ = most_common(binp)

println(ϵ * γ)

function solve(inp)
    ox = map(x -> parse(Int, x, base=2), inp)
    co2 = map(x -> parse(Int, x, base=2), inp)

    p = n
    while length(ox) > 1
        mask = 1 << (p-1)
        ϵ, γ = most_common(map(x->parse.(Int16, [string(x, base=2, pad=n)...]), ox))
        ox = filter(x-> (mask & ϵ & x) > 0 || (mask & ~ϵ & ~x) > 0, ox)
        p -= 1
    end

    p = n
    while length(co2) > 1
        mask = 1 << (p-1)
        ϵ, γ = most_common(map(x->parse.(Int16, [string(x, base=2, pad=n)...]), co2))
        co2 = filter(x-> (mask & γ & x) > 0 || (mask & ~γ & ~x) > 0, co2)
        p -= 1
    end

    return ox[1] * co2[1]
end

println(solve(inp))





