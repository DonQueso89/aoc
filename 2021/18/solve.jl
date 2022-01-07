import Base.convert
import Base.show

infl = "in"

inp = map(eval ∘ Meta.parse, readlines(infl))

MAXV = 9
MAXD = 4

mutable struct Node
    left::Union{Nothing, Node}
    right::Union{Nothing, Node}
    v::Int8
    seq::Int
    depth::Int
end

function exploded(l::Node, r::Node)::Node
    left, right = l.left, r.right
    new = Node(left, right, 0, -1, l.depth - 1)
    if !isnothing(left)
        left.right = new
        left.v += l.v
    end
    if !isnothing(right)
        right.left = new
        right.v += r.v
    end

    new
end

function splitted(n::Node)::Tuple{Node, Node}
    left, right = n.left, n.right
    newl, newr = Node(left, nothing, n.v ÷ 2, -1, n.depth + 1), Node(nothing, right, (n.v + (n.v % 2)) ÷ 2, -1, n.depth + 1)
    newl.right = newr
    newr.left = newl
    if !isnothing(left)
        left.right = newl
    end
    if !isnothing(right)
        right.left = newr
    end

    newl, newr
end

function add(left, right)
    leftmost, rightmost = right, left
    while typeof(leftmost) != Node
        leftmost = leftmost[1]
    end
    while typeof(rightmost) != Node
        rightmost = rightmost[end]
    end

    leftmost.left = rightmost
    rightmost.right = leftmost

    [left, right]
end

show(io::IO, n::Node) = print(io, "Node($(isnothing(n.left) ? -1 : n.left.v), $(n.v), $(isnothing(n.right) ? -1 : n.right.v) (d=$(n.depth)))")

# DFS to make Nodes aware of neighbours
function dfs(inp, G, seq, depth=1)
    inp_ = Any[]
    for v in inp
        if typeof(v) == Int
            node = Node(nothing, nothing, v, seq, depth)
            G[seq] = node
            push!(inp_, node)
            seq += 1
        else
            seq, l = dfs(v, G, seq, depth+1)
            push!(inp_, l)
        end
    end

    return seq, inp_
end

function link_nodes(inp)
    G = Dict()
    _, r = dfs(inp, G, 1)

    for node in values(G)
        node.right = get(G, node.seq+1, nothing)
        node.left = get(G, node.seq-1, nothing)
    end

    r
end

function dfsexploded!(nodes, touched=false)
    for i in 1:length(nodes)
        n = nodes[i]
        if typeof(n) != Node && length(n) == 2 && typeof(n[1]) == Node && typeof(n[2]) == Node && n[1].depth > MAXD && n[2].depth > MAXD
            nodes[i] = exploded(n...)
            touched = true
        elseif typeof(n) != Node
            dfsexploded!(n, touched)
        end
    end

    return touched
end

function dfssplit!(nodes)
    for i in 1:length(nodes)
        n = nodes[i]
        if typeof(n) == Node && n.v > MAXV
            left, right = splitted(n)
            nodes[i] = Any[left, right]
            return true
        elseif typeof(n) != Node
            if dfssplit!(n)
                return true
            end
        end
    end

    return false
end

function reduced(sum_)
    touched = dfsexploded!(sum_)
    touched |= dfssplit!(sum_)
    if touched
        return reduced(sum_)
    end

    return sum_
end

rincr(tree) = ([typeof(x) == Node ? x.depth += 1 : rincr(x) for x in tree])

function magnitude(n)
    if typeof(n) != Node && length(n) == 2
        return 3magnitude(n[1]) + 2magnitude(n[2])
    elseif typeof(n) == Node
        return n.v
    else
        return sum([magnitude(x) for x in n])
    end
end

function solve(terms)
    sum_::Vector{Any} = popfirst!(terms)
    while true
        sum_ = reduced(sum_)
        
        if length(terms) > 0
            term = popfirst!(terms)
            sum_ = add(sum_, term)
            rincr(sum_)
        else
            break
        end

    end

    magnitude(sum_)
end


terms = map(link_nodes, inp)

println(solve(terms))

max_ = 0
for i in 1:length(inp)
    for j in 1:length(inp)
        if i != j
            a, b = link_nodes(inp[i]), link_nodes(inp[j])
            global max_ = max(solve([a, b]), max_)
            a, b = link_nodes(inp[j]), link_nodes(inp[i])
            global max_ = max(solve([a, b]), max_)
        end
    end
end

println(max_)