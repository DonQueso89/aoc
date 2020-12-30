if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = split(read(open(fname), String), "\n\n")
monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""
monster = split(monster, "\n")
monster = transpose(hcat([[y == '#' for y in x] for x in monster[1:end-1]]...)) .== 1

SIZE = Int(sqrt(length(inp)))
MONSTR_SIZE = size(monster)

Option = Union{Nothing, T} where T

mutable struct Tile
    id::Int
    g::BitArray{2}

    # fits
    right:: Option{Tile}
    left:: Option{Tile}
    top:: Option{Tile}
    bottom:: Option{Tile}

    function Tile(id, g)
        new(id, g, nothing, nothing, nothing, nothing)
    end
end

nfits(t::Tile) = sum([t.top, t.bottom, t.left, t.right] .!== nothing)
borders(t::Tile) = (t.g[:,end], t.g[:,1], t.g[1,:], t.g[end,:]) # right, left, top, bottom
right(t::Tile) = borders(t)[1]
left(t::Tile) = borders(t)[2]
top(t::Tile) = borders(t)[3]
bottom(t::Tile) = borders(t)[4]
opposite(f::Function) = Dict(right=>left, left=>right, top=>bottom, bottom=>top)[f]

function tile(s)
    s = split(strip(s), "\n")
    id = parse(Int, s[1][6:9])

    layout = transpose(hcat([[y == '#' for y in x] for x in s[2:end]]...)) .== 1
    return Tile(id, layout)
end

function find_adj!(reftile::Option{Tile}, tiles, border_fn)
  if reftile === nothing
    return
  end
  refside = border_fn(reftile)
  for tile in tiles
    if tile.id == reftile.id
      continue
    end
    for _ = 1:2
      tile.g = reverse(tile.g, dims=2)
      for _=1:4
        tile.g = rotr90(tile.g)
        if all(refside .== opposite(border_fn)(tile))
          return tile
        end
      end
    end
  end
end

function find_adjs(reftile, tiles)
  for fn in [left, right, top, bottom]
    n = find_adj!(reftile, tiles, fn)
    setproperty!(reftile, Symbol(fn), n)
  end
end

tiles = map(tile, inp)
map(x -> find_adjs(x, tiles), tiles)

function assemble()
  corners = [x for x in tiles if nfits(x) == 2]
  topleft = first([x for x in corners if x.top === nothing && x.left === nothing])
  M::Array{Option{Tile}, 2} = fill(nothing, (SIZE, SIZE))
  M[1,1] = topleft
  for y=1:SIZE
    c = M[y,1]
    if y+1<=SIZE
      M[y+1, 1] = find_adj!(c, tiles, bottom)
    end
    for x=1:SIZE
      M[y, x] = c
      c = find_adj!(c, tiles, right)
    end
  end
  return M
end

M = assemble()
println("1: $(reduce(*, [M[1, 1].id, M[1, end].id, M[end, 1].id, M[end, end].id]))")

chopped = (x -> x.g[2:end-1, 2:end-1]).(M)
chopped = hvcat(SIZE, permutedims(chopped)...)
CHOPPED_SIZE = size(chopped)
my, mx = MONSTR_SIZE
cy, cx = CHOPPED_SIZE

function countmonsters(image)
  r = 0
  tot = sum(image)
  monster_weight = sum(monster)
  for y = 1:cy-my+1
    for x = 1:cx-mx+1
      shard = image[y:(y+my-1), x:(x+mx-1)]
      if sum(shard .& monster) == monster_weight
        r += 1
        tot -= monster_weight
      end
    end
  end
  return r, tot
end

for fn in [identity, rot180, rotl90, rotr90]
    n, t = countmonsters(fn(chopped))
    if n > 0
        println("2: $t")
        break
    end
end