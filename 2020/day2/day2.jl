if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input2"
end

input = map(x -> split(x, " "), readlines(infile))

function solve(policies)
    ans1, ans2 = 0, 0
    for policy in policies

        min, max = map(x -> parse(Int32, x), split(policy[1], "-"))
        target = policy[2][1]
        password = policy[3]

        if min <= count(x -> x == target, password) <= max
            ans1 +=1
        end
        
        if count(x -> password[x] == target, [min, max]) == 1
            ans2 +=1
        end

    end
    return ans1, ans2
end


ans1, ans2 = solve(input)

println(ans1)
println(ans2)