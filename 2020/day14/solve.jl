using Combinatorics


if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = readlines(open(fname))

function get_mask(s, meta=false)
    mask = s[8:end]
    additive_mask = parse(Int, replace(mask, r"X"=>"0"), base=2)

    if meta
        subtractive_mask = parse(Int,replace(replace(mask, r"1"=>"0"), r"X"=>"1"), base=2)
    else
        subtractive_mask = parse(Int,replace(mask, r"X"=>"1"), base=2)
    end
    return additive_mask, subtractive_mask
end


mem = Dict{Int, Int}()

additive_mask, subtractive_mask = get_mask(inp[1])
for i in inp[2:end]
    if startswith(i, "mask")
        global additive_mask, subtractive_mask = get_mask(i)
    else
        eval(Meta.parse(i * " & $subtractive_mask | $additive_mask"))
    end
end

function get_meta_meta_masks(meta_mask)
    powers_of_two = []
    n = 0
    while meta_mask > 0
        if meta_mask & 1 == 1
            push!(powers_of_two, 2^n)
        end
        meta_mask >>= 1
        n += 1
    end
    return [map(sum, Combinatorics.combinations(powers_of_two))..., 0]
end

println("1: $(sum(values(mem)))")

mem = Dict{Int, Int}()

base_mask, meta_mask = get_mask(inp[1], true)
meta_meta_masks = get_meta_meta_masks(meta_mask) 
for i in inp[2:end]
    if startswith(i, "mask")
        global base_mask, meta_mask = get_mask(i, true)
        global meta_meta_masks = get_meta_meta_masks(meta_mask)
    else
        addr = parse(Int, match(r"\[(\d+)\]", i).captures[1])
        v = parse(Int, match(r"(\d+)$", i).captures[1])
        
        for meta_meta_mask in meta_meta_masks 
            decoded_mem_addr = (addr | base_mask) & ~meta_mask | meta_meta_mask

            mem[decoded_mem_addr] = v
        end
    end
end
println("2: $(sum(values(mem)))")