import Base.Threads

if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input5"
end
alph = "abcdefghijklmnopqrtsuvwxyz"
polymer = readline(open(fname))

rgx = Regex(join(["$(uppercase(x))$x|$x$(uppercase(x))" for x in alph], "|"))
react(p) = (np = replace(p, rgx=>""); length(np) < length(p) ? react(np) : p;)

println("1: $(length(react(polymer)))")

_min = Threads.Atomic{Int64}(1 << 62)
Threads.@threads for x in alph Threads.atomic_min!(_min, (length ∘ react)(replace(polymer, Regex("[$(uppercase(x)*x)]")=>"")))  end
println("2: $(_min[])")
