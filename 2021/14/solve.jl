infl = "in"

inp = open(infl)
polymer = readline(inp)

t = Dict(map(eval ∘ Meta.parse, split(replace(replace(read(inp, String), "->" => "=>"), r"([A-Z]+)" => s"\"\1\""), "\n")))
N = 40

function solve(polymer, t)
    pairs_ = Dict{String, Int}()
    first_, last_ = polymer[1], polymer[end]

    for i in 2:length(polymer)
        p = String(polymer[i-1:i])
        pairs_[p] = get(pairs_, p, 0) + 1
    end
    it_ = 0
    while it_ < N
        nxt = Dict{String, Int}()
        println(it_)
        keys_ = keys(pairs_)
        for k in keys_
            println(k)
            a, b = String([k[1], t[k][1]]), String([t[k][1], k[2]])
            nxt[a] = get(nxt, a, 0) + pairs_[k]
            nxt[b] = get(nxt, b, 0) + pairs_[k]
        end
        pairs_ = nxt
        it_ += 1
    end
    cnt:: Dict{Char, Float64} = Dict()
    for k in keys(pairs_)
        for c in k
            cnt[c] = get(cnt, c, 0) + pairs_[k]
        end
    end

    for k in keys(cnt)
        cnt[k] /= 2
    end
    cnt[first_] += .5
    cnt[last_] += .5


    maximum(values(cnt)) - minimum(values(cnt))

end

println(solve(polymer, t))

"""

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

NNCB (NN NC CB) -> NC CN NB BC CH HB
NCNBCHB -> NB BC CC CN NB BB BB BC CB BH HC CB
NBCCNBBBCBHCB -> NB BB BB BC CN NC  
NBBBCNCCNBBNBNBBCHBHHBCHB  NB BB 

"""