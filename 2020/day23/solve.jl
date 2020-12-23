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

cups = [parse(Int, x) for x in inp]
dll = Dict()

dll[cups[1]] = (last=10^6, next=cups[2])
dll[10^6] = (last=10^6-1, next=cups[1])

for (i, e) in enumerate(cups[2:end-1])
    dll[e] = (last=cups[i], next=cups[i+2])
end

dll[cups[end]] = (last=cups[end-1], next=10)
dll[10] = (last=cups[end], next=11)

for i = 11:10^6-1
    dll[i] = (last=i-1, next=i+1)
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
    before_seq = dll[e1.last]
    after_seq = dll[e3.next]

    dll[e1.last] = (last=before_seq.last, next=e3.next)
    dll[e3.next] = (last=c, next=after_seq.next)

    dll[c] = (last=e.last, next=e3.next)

    # insert
    before_seq = dll[target]
    after_seq = dll[before_seq.next]

    dll[target] = (last=before_seq.last, next=m1)
    dll[before_seq.next] = (last=m3, next=after_seq.next)

    dll[m1] = (last=target, next=m2)
    dll[m3] = (last=m2, next=before_seq.next)

    global c = e3.next
end

t1 = dll[1].next
t2 = dll[t1].next

println("2: $(t1*t2)")
