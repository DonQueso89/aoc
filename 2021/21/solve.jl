p1 = 8 - 1
p2 = 7 - 1

distr = Dict{Int, Int}(
	3=>1,
	4=>3,
	5=>6,
	6=>7,
	7=>6,
	8=>3,
	9=>1
)
throws = keys(distr)

function solve(throw:: Int, turn:: Bool, p1:: Int, p2 :: Int, s1:: Int, s2:: Int, universes:: Int):: Tuple{Int, Int}
	if turn
		p1 += throw
		p1 %= 10
		s1 += p1 + 1
		if s1 >= 21
			return (universes, 0)
		end
	else
		p2 += throw
		p2 %= 10
		s2 += p2 + 1
		if s2 >= 21
			return (0, universes)
		end
	end

	tot = (0, 0)
	for t in throws
		tot = tot .+ solve(t, !turn, p1, p2, s1, s2, universes * distr[t])
	end

	tot
end

tot = (0, 0)
for t in throws
	global tot
	tot = tot .+ solve(t, true, p1, p2, 0, 0, distr[t])
end

println(tot)