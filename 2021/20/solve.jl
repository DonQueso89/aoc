inp = readlines("in")

algo = []
while length(inp) > 0
    global algo
    line = popfirst!(inp)
    if length(line) > 1
        push!(algo, [c == '#' ? 1 : 0 for c in line]...)
    else
        break
    end
end

algo = convert(BitVector, algo)
img = convert(BitMatrix, collect(transpose(hcat([[c == '#' ? 1 : 0 for c in line] for line in inp]...))))


function enhance(A::BitMatrix, algo::BitVector, f::Function)::BitMatrix
    Y, X = size(A)
    IN::BitMatrix = vcat(f(2, X + 4), hcat(f(Y, 2), A, f(Y, 2)), f(2, X + 4)) 
    OUT::BitMatrix = vcat(f(1, X + 2), hcat(f(Y, 1), similar(A), f(Y, 1)), f(1, X + 2)) 
    offset = CartesianIndex(1, 1)
    C = CartesianIndices(OUT) .+ offset

    for c in C
        kernel = (c - offset):(c + offset)
        S = IN[kernel]
        bin = parse(Int16, string(Int8.([S[1, :]..., S[2, :]..., S[3, :]...])...), base=2)
        OUT[c-offset] = algo[bin + 1]
    end

    OUT
end

function solve(A::BitMatrix, algo::BitVector)::Tuple{Int, Int}
    inf_padder = algo[1] == 0 ? zeros : ones
    alt_inf_padder = inf_padder == ones && algo[512] == 1 ? ones : zeros
    nxtpad = Iterators.cycle([alt_inf_padder, inf_padder])
    A = enhance(A, algo, zeros)
    A = enhance(A, algo, inf_padder)
    r = sum(A)
    n = 48
    for padder in nxtpad
        A = enhance(A, algo, padder)
        n -= 1
        n == 0 && break
    end

    r, sum(A)
end

println(solve(img, algo))
