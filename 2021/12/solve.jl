infl = "in"

inp = readlines(infl)
START = "start"
END = "end"

G = Dict()
for line in inp
	a, b = split(line, '-')
	G[a] = push!(get(G, a, Set()), b)
	G[b] = push!(get(G, b, Set()), a)
end
println(G)

function solve(G, node, path, paths, excl, special)
	if node == END
		push!(paths, path)
	end
	
	for n in setdiff(G[node], [[x for x in path if lowercase(x) == x != special]..., (excl ? [special] : [])...])
		if n == special && n in path
			solve(G, n, [path..., n], paths, true, special)
		else
			solve(G, n, [path..., n], paths, excl, special)
		end
	end
end

paths = Set()

solve(G, START, [START], paths, false, nothing)

println(length(paths))

paths = Set()
small = [x for x in keys(G) if lowercase(x) == x && x != START && x != END]
for x in small
	solve(G, START, [START], paths, false, x)
end
println(length(paths)
