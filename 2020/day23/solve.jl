if length(ARGS) > 0
    inp = "389125467" # test
else
    inp = "327465189"
end

cups = [parse(Int, x) for x in inp]
for _=1:100
    c = cups[1]
    movers = cups[2:4]
    stayers = cups[5:end]
    target = c-1 < 1 ? 9 : c-1
    target_idx = findfirst(x -> x == target, stayers)
    while target_idx === nothing
        target = target-1 < 1 ? 9 : target-1
        target_idx = findfirst(x -> x == target, stayers)
    end
    global cups = [stayers[1:target_idx]..., movers..., stayers[target_idx+1:end]..., c]
end

idx = findfirst(isone, cups)
println("1: $(join(circshift(cups, -idx)[1:end-1]))")

mutable struct E
    last::Int
    next::Int
end


cups = [parse(Int, x) for x in inp]
dll = Dict()
dll[cups[1]] = E(10^6, cups[2])
dll[10^6] = E(10^6-1, cups[1])

for (i, e) in enumerate(cups[2:end-1])
    dll[e] = E(cups[i], cups[i+2])
end

dll[cups[end]] = E(cups[end-1], 10)
dll[10] = E(cups[end], 11)

for i = 11:10^6-1
    dll[i] = E(i-1, i+1)
end

c = 3
for i=1:10^7
    e = dll[c]
    m1 = e.next
    m2 = dll[m1].next
    m3 = dll[m2].next
    target = (c - 1) < 1 ? 10^6 : c - 1
    while target in [m1, m2, m3]
        target = (target - 1) < 1 ? 10^6 : target - 1
    end

    e1 = dll[m1]
    e3 = dll[m3]

    # remove
    dll[e1.last].next = e3.next
    dll[e3.next].last = c

    dll[c].next = e3.next

    # insert
    mem = dll[target].next
    dll[target].next = m1
    dll[mem].last = m3

    dll[m1].last = target
    dll[m3].next = mem

    global c = dll[c].next
end

t1 = dll[1].next
t2 = dll[t1].next

println("2: $(t1*t2)")
