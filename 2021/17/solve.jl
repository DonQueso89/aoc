in = [[94, -156], [151, -103]]
tin = [[20, -10], [30, -5]]

function solve(ll, ur)
    max_ = -Inf
    maxv = nothing
    hits = Set()
    llx, lly = ll
    urx, ury = ur
    for x in -500:500
        for y in -500:500
            velo = [x, y]
            pos = [0, 0]
            my = -Inf
            while true
                px, py = pos
                pos += velo
                vx, _ = velo
                velo -= [vx == 0 ? 0 : vx > 0 ? 1 : -1, 1]
                my = max(my, pos[2])

                if px > urx || py < lly
                    break
                end

                if llx <= px <= urx && lly <= py <= ury
                    push!(hits, (x, y))
                    if my > max_
                        max_ = my
                        maxv = (x, y)
                    end
                    break
                end
            end
        end
    end

    maxv, max_, length(hits)

end

println(solve(in...))