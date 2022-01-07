import Base.maximum
import Base.minimum

HSIZE = 3
LSIZE = 5
LTYPE = 4
LMODE = 0
LMODESIZE = 15
NMODE = 1
NMODESIZE = 11

infl = "in"
prs(s::Union{String, Char}) = parse(Int128, s, base=2)
bin(s::Union{Char, String})::String = string(parse(Int, s, base=16), base=2, pad=4)
inp = string(map(bin, collect(read(open(infl), String)))...)

function op(s::String)::Tuple{Int, Int, String, Function}
    mode = prs(s[1])
    size_ = mode == LMODE ? LMODESIZE : NMODESIZE
    mode, prs(s[2:size_+1]), s[2+size_:end], version
end

function type(s::String)::Tuple{Int, String, Function}
    t = prs(s[1:HSIZE])
    if t == LTYPE
        t, s[HSIZE+1:end], literal
    else
        t, s[HSIZE+1:end], op
    end
end

function version(s::String)::Tuple{Int, String, Function}
    v = prs(s[1:HSIZE])
    v, s[HSIZE+1:end], type
end

function literal(s::String)::Tuple{Int, String, Function, Int}
    r = ""
    chompsize = 0
    while true
        chunk, s = s[1:LSIZE], s[LSIZE+1:end]
        chompsize += 5
        r = string(r, chunk[2:end])
        if first(chunk) == '0'
            return parse(Int, r, base=2), s, version, chompsize
        end
    end
end

min_(args...) = minimum(args)
max_(args...) = maximum(args)

OPS = Dict(
    0=>+,
    1=>*,
    2=>min_,
    3=>max_,
    5=>>,
    6=><,
    7=>==,
)
function solve(bs:: String, mode::Int, npackets::Int, outer_op::Function=identity, r::Int=0)
    r = 0
    next_op = version
    args = []
    v = nothing
    while true
        if npackets == 0
            return bs, outer_op(args...), r
        end

        if next_op == op
            mode_, npackets_, bs_, next_op = next_op(bs)
            bs, arg, r_ = solve(bs_, mode_, mode_ == LMODE ? npackets_ : 3npackets_ , OPS[v], r)
            push!(args, arg)
            r+=r_
            npackets -= mode == LMODE ? (1 + (mode_ == LMODE ? LMODESIZE : NMODESIZE) + length(bs_) - length(bs)) : 1
        elseif next_op == version
            v, bs, next_op = next_op(bs)
            r += v
            npackets -= mode == LMODE ? HSIZE : 1
        elseif next_op == literal
            v, bs, next_op, chompsize = next_op(bs)
            push!(args, v)
            npackets -= mode == LMODE ? chompsize : 1
        else
            v, bs, next_op = next_op(bs)
            npackets -= mode == LMODE ? HSIZE : 1
        end
    end
end

println(solve(inp, NMODE, 3))