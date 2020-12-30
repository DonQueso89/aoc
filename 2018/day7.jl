if length(ARGS) > 0
  fname = ARGS[1]
else
  fname = "input7"
end

inp = readlines(open(fname))
nodes = Set{Symbol}()

for line in inp
  downstream = line[end-11]
  upstream = line[6]
  expr = "(@isdefined $upstream) ? nothing : $upstream = Set()"
  eval(Meta.parse(expr))
  expr = "(@isdefined $downstream) ? push!($downstream, '$upstream') : $downstream = Set(['$upstream'])"
  eval(Meta.parse(expr))
  push!(nodes, Symbol(upstream), Symbol(downstream))
end

n_nodes = length(nodes)
order = []

while length(order) < n_nodes
  cur = sort([nodes...], by=x -> (length(eval(x)), String(x)[1])) |> first
  push!(order, pop!(nodes, cur))

  for node in nodes
    pop!(eval(node), String(cur)[1], nothing)
  end
end

println("1: $(join(order))")


