import Base.display


if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

inp = split(read(open(fname), String), "\n\n")

mutable struct Tile
    id::Int
    g::BitArray{2}

    # fits
    right:: Array{Tile}
    left:: Array{Tile}
    top:: Array{Tile}
    bottom:: Array{Tile}

    nfits::Int
    oriented::Bool

    function Tile(id, g)
        new(id, g, [], [], [], [], 0, false)
    end
end

display(t::Tile) = display(t.g)
borders(t::Tile) = (t.g[:,end], t.g[:,1], t.g[1,:], t.g[end,:]) # right, left, top, bottom
section(t::Tile) = println("\n     $(length(t.top) > 0 ? t.top[1].id : "XXXX")     \n$(length(t.left) > 0 ? t.left[1].id : "XXXX") $(t.id) $(length(t.right) > 0 ? t.right[1].id : "XXXX")\n     $(length(t.bottom) > 0 ? t.bottom[1].id : "XXXX")     ")
function tile(s)
    s = split(s, "\n")
    id = parse(Int, s[1][6:9])

    layout = s = transpose(hcat([[y == '#' for y in x] for x in s[2:end]]...)) .== 1
    return Tile(id, layout)
end

function bootstrap(last_oriented_tile, tiles)
    # orient 1 pair, then find the rest
    left_adj, right_adj, top_adj, bottom_adj = nothing, nothing, nothing, nothing
    for tile in tiles
        if tile.id == last_oriented_tile.id
            continue
        end

        right, left, top, bottom = borders(last_oriented_tile)
        for flipfn in [reverse, reverse]
            tile.g = flipfn(tile.g, dims=2)
            for rotfn in [rotr90, rotr90, rotr90, rotr90]
                tile.g = rotfn(tile.g)
                tright, tleft, ttop, tbottom = borders(tile)

                if length(last_oriented_tile.left) == 0 && all(tright .== left)
                    push!(tile.right, last_oriented_tile)
                    push!(last_oriented_tile.left, tile)
                    tile.oriented = true
                    left_adj = tile
                    break
                elseif length(last_oriented_tile.right) == 0 && all(tleft .== right)
                    push!(tile.left, last_oriented_tile)
                    push!(last_oriented_tile.right, tile)
                    tile.oriented = true
                    right_adj = tile
                    break
                elseif length(last_oriented_tile.bottom) == 0 && all(ttop .== bottom)
                    push!(tile.top, last_oriented_tile)
                    push!(last_oriented_tile.bottom, tile)
                    tile.oriented = true
                    bottom_adj = tile
                    break
                elseif length(last_oriented_tile.top) == 0 && all(tbottom .== top)
                    push!(tile.bottom, last_oriented_tile)
                    push!(last_oriented_tile.top, tile)
                    tile.oriented = true
                    top_adj = tile
                    break
                end
            end
        end
    end
end


tiles = map(tile, inp)
println(length(tiles))