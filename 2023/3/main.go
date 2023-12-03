package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"slices"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

var deltas = [8][2]int{
	{-1, 1},
	{1, 0},
	{0, 1},
	{1, 1},
	{0, -1},
	{-1, 0},
	{-1, -1},
	{1, -1},
}

type YX = struct {
	y int
	x int
	v int
}

var symbols = []rune{'/', '&', '%', '$', '+', '@', '=', '-', '#', '*'}

func isAdjacent(y int, x int, grid []string, adjMatrix *[]YX) bool {
	isAdj := false
	for _, a := range deltas {
		dy, dx := a[0]+y, a[1]+x
		if 0 <= dy && dy < len(grid) && 0 <= dx && dx < len(grid[y]) {
			if slices.Contains[[]rune, rune](symbols, rune(grid[dy][dx])) {
				isAdj = true
			}
			gear := YX{dy, dx, 0}
			if grid[dy][dx]-'*' == 0 && !slices.Contains[[]YX, YX](*adjMatrix, gear) {
				*adjMatrix = append(*adjMatrix, gear)
			}
		}
	}
	return isAdj
}

func main() {
	var testing bool
	flag.BoolVar(&testing, "test", false, "--test to Run with test input")
	flag.Parse()

	fname := "in"
	if testing {
		fname = "test"
	}

	data, err := os.ReadFile(fname)
	check(err)

	grid := strings.Split(string(data), "\n")
	exp := 0.0
	isPart := false
	curNum := 0.0
	s := 0
	adj := make([]YX, 0)
	gears := make(map[YX][]int, 0)
	for y := len(grid) - 1; y >= 0; y-- {
		row := grid[y]
		for x := len(row) - 1; x >= 0; x-- {
			r := row[x]
			i := int(r - '0')
			switch {
			case r == '.' || slices.Contains[[]rune, rune](symbols, rune(r)):
				if isPart {
					s += int(curNum)
				}
				for _, gear := range adj {
					_, ok := gears[gear]
					if ok {
						gears[gear] = append(gears[gear], int(curNum))
					} else {
						gears[gear] = []int{int(curNum)}
					}
				}
				exp = 0
				curNum = 0
				isPart = false
				adj = make([]YX, 0)
			case 0 <= i && i <= 9:
				curNum += float64(i) * math.Pow(10, exp)
				exp++
				isPart = isPart || isAdjacent(y, x, grid, &adj)
			}
		}
	}
	if isPart {
		s += int(curNum)
		isPart = false
	}
	for _, gear := range adj {
		_, ok := gears[gear]
		if ok {
			gears[gear] = append(gears[gear], int(curNum))
		} else {
			gears[gear] = []int{int(curNum)}
		}
	}
	fmt.Println(s)

	s2 := 0
	for _, v := range gears {
		if len(v) == 2 {
			s2 += v[0] * v[1]
		}
	}
	fmt.Println(s2)
}
