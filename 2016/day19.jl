# possible alternative: something with subtracting consecutive arithmetic series
S(a0, an, s) = (an^2 - a0^2 + s*(an+a0)) / 2s # arbitrary arithmetic series
function solve(len, first, last, step)
    if len == 1
        return first
    end
    if len % 2 == 0
        return solve(len / 2, first, last-step, step*2)
    end
    return solve((len - 1) / 2, first+step*2, last, step*2)
end

n = 3012210

println(solve(n, 1, n, 1))


# Second solution is only completed for even n (laziness)
mutable struct Node
  v:: Int64
  nxt:: Node
  Node(v::Int64) = (tmp = new(v); tmp.nxt = tmp)
end

function circle(n)
           root = Node(n)
           tmp = root
           initial = tmp
           for i in (n-1):-1:1
               tmp_ = Node(i)
               tmp_.nxt = tmp
               tmp = tmp_
               if i == n / 2
                   initial = tmp
               end
           end
           root.nxt = tmp
           return initial
       end

function solve2(n)
  voor_pineut = circle(n)
  even = true
  while voor_pineut.nxt != voor_pineut
    pineut = voor_pineut.nxt
    #println("Eliminating ", pineut.v)
    voor_pineut.nxt = pineut.nxt
    even = !even

    if even
      voor_pineut = pineut.nxt
    end
  end
  return voor_pineut
end

println(solve2(n))
