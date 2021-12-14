infl = "in"

inp = open(infl)
polymer = readline(inp)

t = Dict(map(eval ∘ Meta.parse, split(replace(replace(read(inp, String), "->" => "=>"), r"([A-Z]+)" => s"\"\1\""), "\n")))
NULL = 'n'
N = 40

mutable struct E
    left::Union{Char, E}
    right::Union{Char, E}
    v::Char
end
println(polymer)
println(t)
function solve(polymer, t)
    d = Dict{Char, Int}()

    entry = E(E(NULL, NULL, polymer[1]), NULL, polymer[2])
    prev = entry
    for c in polymer[3:end]
        cur = E(prev, NULL, c)
        prev.right = cur
        prev = cur
    end

    for c in polymer
        d[c] = get(d, c, 0) + 1
    end

    n = 0
    while n < 20
        cur = entry
        entry = nothing
        while cur != NULL
            s = String([cur.left.v, cur.v])
            repl = t[s][1]
            insert_ = E(cur.left, cur, repl)
            cur.left.right = insert_
            cur.left = insert_
            if isnothing(entry)
                entry = insert_
            end
            d[repl] = get(d, repl, 0) + 1
            cur = cur.right
        end
        n+=1
    end

   maximum(values(d)) - minimum(values(d)), sum(values(d))

end

println(solve(polymer, t))

e = E(NULL, NULL, NULL)