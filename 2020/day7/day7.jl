if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input7"
end

input = readlines(infile)
GOLD = "shiny gold bag"

tobag(b) = b == "no other bag" ? (n=0, clr=nothing) : (n=parse(Int32, b[1]), clr=rstrip(SubString(b, 3:length(b)), 's'))

function can_haz_gold(item, lkp)
    if item === nothing
        return false
    elseif item == GOLD
        return true
    else
        bags = lkp[item]
        return any([can_haz_gold(x.clr, lkp) for x in bags])
    end
end

function sum_bags(bag, lkp)
    bags = get(lkp, bag.clr, nothing)

    if bags === nothing
        return bag.n
    end
    
    return bag.n + bag.n * sum([sum_bags(b, lkp) for b in bags])
end

function solve(lines)
    lines = map(x -> split(rstrip(replace(x, r"bags" => "bag"), '.'), " contain "), lines)
    lookup = Dict([(x[1], map(tobag, split(x[2], ", "))) for x in lines])


    return sum([b != GOLD ? can_haz_gold(b, lookup) : false for b in keys(lookup)]), sum_bags((clr=GOLD, n=1), lookup) - 1
end

a, b = solve(input)

println("1: $a")
println("1: $b")