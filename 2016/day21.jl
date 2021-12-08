import Base.findfirst
infl = "input21"
inp = readlines(infl)

v = ["abcdefgh"...]
ff(x, a) = findfirst(z -> z == x, a)


swap(arr::Vector{Char}, x::Int8, y::Int8) = (t = arr[x]; arr[x] = arr[y]; arr[y] = t; arr)
swap(arr::Vector{Char}, x::Char, y::Char) = (x::Int8 = ff(x, arr); y::Int8 = ff(y, arr); swap(arr, x, y))
circshift(arr::Vector{Char}, d::String, )

println(swap(v, Int8(3), Int8(5)))
println(swap(v, 'a', 'f'))
