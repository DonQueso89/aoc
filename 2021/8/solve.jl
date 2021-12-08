import Base.Iterators.product

infl = "in"

inp = readlines(infl)

segments = "abcdefg"


zero = Set(['a', 'b', 'c', 'e', 'f', 'g'])
one = Set(['c', 'f'])
two = Set(['a', 'c', 'd', 'e', 'g'])
three = Set(['a', 'c', 'd', 'f', 'g'])
four = Set(['b', 'c', 'd', 'f'])
five = Set(['a', 'b', 'd', 'f', 'g'])
six = Set(['a', 'b', 'd', 'f', 'e', 'g'])
seven = Set(['a', 'c', 'f'])
eight = Set([segments...])
nine = Set(['a', 'b', 'c', 'd', 'f', 'g'])

lunique = Set([2,4,7,3])

bylength = Dict([2=>[one], 4=>[four], 7=>[eight], 3=>[seven], 6=>[nine, six, zero], 5=>[five, three, two]])

numbers = [zero, one, two, three, four, five, six, seven, eight, nine]
bynum = Dict(numbers[i+1]=>i for i in 0:9)

function solve(inp)
    r = 0
    for x in inp
        x = split(strip.(split(x, '|'))[2])
        r += length([y for y in x if length(y) in lunique])
    end
    println(r)
end

function sortsignals(a, b)
    if length(a) in lunique
        true
    elseif length(b) in lunique
        false
    else
        isless(length(a), length(b))
    end
end

function solve2(inp)
    r = 0
    for x in inp
        tracker = Dict([c=>Set([segments...]) for c in segments])
        signals, output = strip.(split(x, '|'))
        signals, output = split(signals), split(output)
        sort!(signals, lt=sortsignals)

        for c in segments
            impossible = union([union(bylength[length(s)]...) for s in signals if c ∉ s && length(s) in lunique]..., 'z')
            tracker[c] = setdiff(tracker[c], impossible)

            for s in signals
                if c ∈ s
                    tracker[c] = intersect(tracker[c], setdiff(union(bylength[length(s)]...), impossible))
                end
            end

        end
        
        # Brute force it from here for lack of creativity
        mappings = [[k=>v for v in tracker[k]] for k in keys(tracker)]
        mapping_found = false
        for mapping in product(mappings...)
            mapping = Dict(mapping)
            
            result = Set()
            for s in signals
                mapped = Set([mapping[c] for c in s])
                if mapped in numbers
                    push!(result, mapped)
                end
            end
            
            if length(result) == 10
                mapping_found = true
                for (pow, o) in enumerate(output)
                    mapped = Set([mapping[c] for c in o])
                    print(bynum[mapped])
                end
                println()
            end

            if mapping_found
                break
            end
        end
    end
end

solve2(inp)
