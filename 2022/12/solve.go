package main

import "log"
import "os"
import "bytes"
import u "aoc/utils"
import "fmt"
import "strings"

type Vertex struct {
	height byte
	dist int
}

type Pos struct {
	y int
	x int
}
type Grid map[Pos]*Vertex

func (p *Pos) String() string {
	return fmt.Sprintf("<y: %d x: %d>", p.y, p.x)
}

func (v *Vertex) String() string {
	return fmt.Sprintf("<height: %s dist: %d>", string(v.height), v.dist)
}

func (grid *Grid) String(Y, X int, ST, E *Pos) string {
	var s strings.Builder
	for i := 0; i < 3; i++ {
		for x := 0; x < X; x++ {
			fmt.Fprintf(&s, string(fmt.Sprintf("%03d\n", x)[i]))
		}
		s.WriteString("\n")
	}
	for y := 0; y < Y; y++ {
		for x := 0; x < X; x++ {
			p := Pos{y, x}
			if (*grid)[p].dist > 0 {
				fmt.Fprintf(&s, "*")
			} else if p == *E {
				fmt.Fprintf(&s, "E")
			} else if p == *ST {
				fmt.Fprintf(&s, "S")
			}else {
				fmt.Fprintf(&s, string((*grid)[p].height))
			}
		}
		fmt.Fprintf(&s, "%d", y)
		s.WriteString("\n")
	}
	return s.String()
}

const END = 69
const START = 83
const MINHEIGHT = 97
const MAXHEIGHT = 122

func down(p *Pos) *Pos {
	return &Pos{p.y+1, p.x}
} 
func up(p *Pos) *Pos {
	return &Pos{p.y-1, p.x}
} 
func left(p *Pos) *Pos {
	return &Pos{p.y, p.x-1}
} 
func right(p *Pos) *Pos {
	return &Pos{p.y, p.x+1}
}

func options(p *Pos, grid *Grid, S *Pos) []*Pos {
	var result []*Pos
	vertex := (*grid)[*p]
	for _, n := range [4]*Pos{down(p), up(p), left(p), right(p)} {
		adjVertex, ok := (*grid)[*n]
		if !ok {
			continue
		}
		if *n == *S || int8(adjVertex.height) - int8(vertex.height) > 1 || adjVertex.dist > 0 {
			continue
		}
		result = append(result, n)
	}
	return result
}


func floodfill(grid Grid, start *Pos, end *Pos) Vertex {
	scouts := []*Pos{start}
	for {
		newScouts := make([]*Pos, 0)
		for _, scout := range scouts {
			vertex := grid[*scout]
			adjacent := options(scout, &grid, start)
			for _, adj := range adjacent {
				adjVertex := grid[*adj]
				adjVertex.dist = vertex.dist + 1
				newScouts = append(newScouts, adj)
			}
		}
		scouts = newScouts
		if len(scouts) == 0 {
			break
		}
	}
	return *grid[*end]
}

func (grid *Grid) reset() {
	for _, vertex := range *grid {
		vertex.dist = 0 
	}
}

func main() {
	log.SetFlags(0)
	content, err := os.ReadFile("inp.txt")
	u.Must(err)
	lines := bytes.Split(content, []byte("\n"))
	scouts := make([]*Pos, 0)
	grid := make(Grid)
	var start, end *Pos

	// Setup
	for y, row := range lines {
		for x, height := range row {
			if height == START {
				start = &Pos{y, x}
				scouts = append(scouts, start)
				grid[*start] = &Vertex{MINHEIGHT, 0}
			} else if height == END {
				end = &Pos{y, x}
				grid[*end] = &Vertex{MAXHEIGHT, 0}
			} else {
				grid[Pos{y, x}] = &Vertex{height, 0}
			}
		}
	}

	min := floodfill(grid, start, end).dist
	fmt.Printf("1: %v\n", min)
	grid.reset()
	for pos, vertex := range grid {
		if vertex.height == MINHEIGHT {
			v := floodfill(grid, &pos, end)
			if v.dist > 0 && v.dist < min {
				min = v.dist
			}
			grid.reset()
		}
	}
	fmt.Printf("2: %v\n", min)

}