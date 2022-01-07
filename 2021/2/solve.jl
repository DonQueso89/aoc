inp = map(x->(x[1][1], parse(Int, x[2])), split.(readlines("in")))

println(prod(sum([x[2]*Dict('f'=>1, 'u'=>0, 'd'=>0)[x[1]], x[2]*Dict('f'=>0, 'u'=>-1, 'd'=>1)[x[1]]] for x in inp)))

m(x, y, a, op, v) = (op == 'f' ? [x+v, y+a*v, a] : op == 'u' ? [x, y, a-v] : [x, y, a+v])

println(reduce(*,(foldl((a,e)->m(a...,e...),inp, init=[0,0,0]))[1:2]))
