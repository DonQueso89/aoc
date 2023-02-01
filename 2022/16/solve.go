package main

import (
	u "aoc/utils"
	"fmt"
	"os"
	re "regexp"
	"strconv"
	"strings"
)

type Vertex struct {
	val    string
	rate   int
	edges  []string
	dists  map[string]int
	score  int
	dscore int
}

type Path struct {
	score int
	steps int
	v     *Vertex
	done  map[string]bool
}
type DPath struct {
	score    int
	vSteps   int
	wSteps   int
	v        *Vertex
	w        *Vertex
	done     map[string]bool
	depleted bool
}

func (v *Vertex) String() string {
	return fmt.Sprintf("%s (%d) -> %v", v.val, v.rate, v.edges)
}
func (p *Path) String() string {
	return fmt.Sprintf("score: %d steps: %d cur: %v", p.score, p.steps, p.v.val)
}

func (v *Vertex) distances(graph map[string]*Vertex) map[string]int {
	d := make(map[string]int)
	dist := 0
	cur := []*Vertex{v}
	for {
		edges := make([]*Vertex, 0)
		for i := range cur {
			e := cur[i]
			_, visited := d[e.val]
			if !visited {
				d[e.val] = dist
			}
			edges = append(
				edges,
				u.Map[string, *Vertex](e.edges, func(s string) *Vertex { return graph[s] })...,
			)
		}
		dist++
		cur = edges

		if len(d) == len(graph) {
			for k, v := range graph {
				if v.rate == 0 {
					delete(d, k)
				}
			}
			return d
		}
	}

}

func main() {
	data, ok := os.ReadFile(u.GetInputFile())
	u.Must(ok)
	lines := strings.Split(string(data), "\n")

	graph := make(map[string]*Vertex)
	patt := re.MustCompile(`[A-Z]{2}|\d+`)

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		elems := patt.FindAllString(line, -1)
		rate, ok := strconv.ParseInt(elems[1], 10, 8)
		u.Must(ok)
		graph[elems[0]] = &Vertex{elems[0], int(rate), elems[2:], nil, 0, 0}
	}

	for k, v := range graph {
		if v.rate > 0 || k == "AA" {
			v.dists = v.distances(graph)
		}
	}

	max := 0
	dmax := 0
	paths := []*Path{&Path{0, 30, graph["AA"], make(map[string]bool)}}
	dpaths := []*DPath{&DPath{0, 26, 26, graph["AA"], graph["AA"], make(map[string]bool), false}}
	d := make(map[string]bool)

	for {
		var newPaths []*Path
		for i := range paths {
			path := paths[i]
			var candidates []*Path
			for k, dist := range path.v.dists {
				target := graph[k]
				score := (path.steps - (dist + 1)) * target.rate
				if path.score+score > target.score && path.steps-(dist+1) >= 0 && !path.done[target.val] {
					done := u.CopyMap(path.done)
					done[k] = true
					candidates = append(candidates, &Path{path.score + score, path.steps - (dist + 1), target, done})
				}
			}

			if len(candidates) > 0 {
				newPaths = append(newPaths, candidates...)
			} else {
				max = u.Max(max, path.score)
			}
		}

		paths = newPaths

		var newDPaths []*DPath
		for i := range dpaths {
			path := dpaths[i]

			// Distance from current max is a wet finger heuristic that actually works
			if path.depleted || (dmax-path.score) > 0 && (dmax-path.score) > 10 {
				continue
			}
			var candidates []*DPath

			for vt, dist := range path.v.dists {
				for wt, wDist := range path.w.dists {
					if vt == wt || (len(dpaths) == 1 && d[fmt.Sprintf("%s%s", wt, vt)]) {
						continue
					}
					d[fmt.Sprintf("%s%s", vt, wt)] = true
					target := graph[vt]
					wTarget := graph[wt]

					candidate := &DPath{path.score, path.vSteps, path.wSteps, path.v, path.w, u.CopyMap(path.done), false}

					score := (path.vSteps - (dist + 1)) * target.rate
					if path.score+score > target.dscore && path.vSteps-(dist+1) >= 0 && !path.done[target.val] {
						candidate.done[vt] = true
						candidate.score += score
						candidate.vSteps -= dist + 1
						candidate.v = target
					}

					score = (path.wSteps - (wDist + 1)) * wTarget.rate
					if path.score+score > wTarget.dscore && path.wSteps-(dist+1) >= 0 && !candidate.done[wTarget.val] {
						candidate.done[wt] = true
						candidate.score += score
						candidate.wSteps -= wDist + 1
						candidate.w = wTarget
					}
					if candidate.score > path.score {
						candidates = append(candidates, candidate)
					}
				}
			}

			if len(candidates) > 0 {
				newDPaths = append(newDPaths, candidates...)
			} else {
				path.depleted = true
				dmax = u.Max(dmax, path.score)
			}
		}

		dpaths = newDPaths
		if len(paths)+len(dpaths) == 0 {
			break
		}
	}

	fmt.Println(max)
	fmt.Println(dmax)
}
