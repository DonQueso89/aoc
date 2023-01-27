package main

import (
	u "aoc/utils"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type XYZ struct {
	x int
	y int
	z int
}

func (v *XYZ) String() string {
	return fmt.Sprintf("<%d %d %d>", v.x, v.y, v.z)
}

func (v *XYZ) neighbours() []*XYZ {
	return []*XYZ{
		&XYZ{v.x - 1, v.y, v.z},
		&XYZ{v.x + 1, v.y, v.z},
		&XYZ{v.x, v.y + 1, v.z},
		&XYZ{v.x, v.y - 1, v.z},
		&XYZ{v.x, v.y, v.z + 1},
		&XYZ{v.x, v.y, v.z - 1},
	}
}

func exposedSurface(positions *map[XYZ]bool) int {
	exposed := len(*positions) * 6
	for p, _ := range *positions {
		for _, n := range p.neighbours() {
			if (*positions)[*n] {
				exposed--
			}
		}
	}
	return exposed
}

func (v *XYZ) withinBounds(minX, minY, minZ, maxX, maxY, maxZ int) bool {
	return v.x >= minX && v.x <= maxX && v.y >= minY && v.y <= maxY && v.z >= minZ && v.z <= maxZ
}

func main() {
	data, ok := os.ReadFile(u.GetInputFile())
	u.Must(ok)
	lines := strings.Split(string(data), "\n")

	var xBound, yBound, zBound int
	occupied := make(map[XYZ]bool)
	_ = u.Map[string, *XYZ](lines, func(s string) *XYZ {
		elems := u.Map[string, int](strings.Split(s, ","), func(e string) int {
			i, ok := strconv.ParseInt(e, 10, 8)
			u.Must(ok)
			return int(i)
		})
		p := XYZ{elems[0], elems[1], elems[2]}
		occupied[p] = true
		if elems[0] > xBound {
			xBound = elems[0]
		}
		if elems[1] > yBound {
			yBound = elems[1]
		}
		if elems[2] > zBound {
			zBound = elems[2]
		}
		return &p
	})

	exposed := exposedSurface(&occupied)
	fmt.Println(exposed)

	outsideComplement := make(map[XYZ]bool)
	// floodfill
	cur := map[XYZ]bool{XYZ{-1, -1, -1}: true}
	for {
		next := make(map[XYZ]bool)
		for k, _ := range cur {
			outsideComplement[k] = true
		}

		for k, _ := range cur {
			for _, n := range k.neighbours() {
				if occupied[*n] || outsideComplement[*n] {
					continue
				}
				if n.withinBounds(-1, -1, -1, xBound+1, yBound+1, zBound+1) {
					next[*n] = true
				}
			}
		}
		cur = next
		if len(cur) == 0 {
			break
		}
	}

	outsideSurface := 0
	for v, _ := range occupied {
		for _, n := range v.neighbours() {
			if outsideComplement[*n] {
				outsideSurface++
			}
		}
	}

	fmt.Println(outsideSurface)
}
