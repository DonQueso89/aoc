package main

import (
	u "aoc/utils"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type YX struct {
	y int
	x int
}

func (p *YX) down() *YX {
	return &YX{p.y + 1, p.x}
}
func (p *YX) left() *YX {
	return &YX{p.y, p.x - 1}
}
func (p *YX) right() *YX {
	return &YX{p.y, p.x + 1}
}

type Grid map[YX]byte

const FREE = 46
const ROCK = 35
const SAND = 111

var START = YX{0, 500}

func (g *Grid) String() string {
	s := strings.Builder{}
	for y := 0; y < 200; y++ {
		s.WriteString("\n")
		for x := 200; x < 800; x++ {
			e, ok := (*g)[YX{y, x}]
			if ok {
				s.WriteString(string(e))
			} else {
				s.WriteString(string(FREE))
			}

		}
	}

	return s.String()
}

func stoi(s string) int {
	i, _ := strconv.ParseInt(s, 10, 16)
	return int(i)
}

func swap(a, b int) (int, int) {
	a += b
	b = a - b
	a -= b
	return a, b
}

func solve(g *Grid, stopCondition func(*YX) bool) int {
	cur := &YX{START.y, START.x}
	nrest := 0
	for {
		cur = &YX{START.y, START.x}

		for {
			next := cur.down()
			_, ok := (*g)[*next]
			if !ok {
				cur = next
				continue
			}

			next = next.left()
			_, ok = (*g)[*next]
			if !ok {
				cur = next
				continue
			}

			next = (*next.right()).right()
			_, ok = (*g)[*next]
			if !ok {
				cur = next
				continue
			}

			(*g)[*cur] = SAND
			nrest++
			if stopCondition(cur) {
				return nrest
			}

			break
		}
	}
}

func freshGrid(lines []string) (*Grid, int) {
	grid := make(Grid)
	maxy := 0
	for _, line := range lines {
		v := strings.Split(line, " -> ")

		if len(v) <= 1 {
			continue
		}

		var sx, sy, x, y int
		for i, c := range v[1:] {
			e := strings.Split(c, ",")
			s := strings.Split(v[i], ",")
			parsed := u.Map[string, int]([]string{s[0], s[1], e[0], e[1]}, stoi)
			sx, sy, x, y = parsed[0], parsed[1], parsed[2], parsed[3]
			if sx > x {
				sx, x = swap(sx, x)
			}
			if sy > y {
				sy, y = swap(sy, y)
			}

			if y > maxy {
				maxy = y
			}

			for iy := sy; iy <= y; iy++ {
				for ix := sx; ix <= x; ix++ {
					grid[YX{iy, ix}] = ROCK
				}
			}
		}
	}

	for x := 0; x <= 1000; x++ {
		grid[YX{maxy + 2, x}] = ROCK
	}

	return &grid, maxy

}

func main() {
	data, err := os.ReadFile("inp.txt")
	u.Must(err)
	lines := strings.Split(string(data), "\n")
	grid, maxy := freshGrid(lines)
	fmt.Println(solve(grid, func(p *YX) bool {
		return p.y == maxy+1
	}) - 1)

	grid, _ = freshGrid(lines)
	fmt.Println(solve(grid, func(p *YX) bool {
		return *p == START
	}))

	//fmt.Println(grid)
}
