package main

import (
	"fmt"
	u "aoc/utils"
	"os"
	"strings"
)

type YX = u.YX

const XBOUND = 7
const LEFT = 60
const RIGHT = 62

const MINUS = 0
const PLUS = 1
const L = 2
const I = 3
const SQUARE = 4

var allKinds = [5]int{MINUS, PLUS, L, I, SQUARE}

type Rock struct {
	shape []*YX
	width int
	height int
	offset int
	rOffset int
}

func create(kind int, topR *YX) *Rock {
	y := topR.Y
	x := topR.X
	switch kind {
		case MINUS:
			return &Rock{[]*YX{&YX{y, x}, &YX{y, x-3}, &YX{y, x-2}, &YX{y, x-1}}, 4, 1, 3, 0}
		case PLUS:
			return &Rock{[]*YX{&YX{y, x}, &YX{y-1, x}, &YX{y-2, x}, &YX{y-1, x+1}, &YX{y-1, x-1}}, 3, 3, 1, 1}
		case L:
			return &Rock{[]*YX{&YX{y, x}, &YX{y-1, x}, &YX{y-2, x}, &YX{y-2, x-1}, &YX{y-2, x-2}}, 3, 3, 2, 0}
		case I:
			return &Rock{[]*YX{&YX{y, x}, &YX{y-1, x}, &YX{y-2, x}, &YX{y-3, x}}, 1, 4, 0, 0}
		case SQUARE:
			return &Rock{[]*YX{&YX{y, x}, &YX{y-1, x}, &YX{y-1, x-1}, &YX{y, x-1}}, 2, 2, 1, 0}
		default:
			return &Rock{}
	}
}

func (r *Rock) down() {
	for _, s := range r.shape {
		s.Y -= 1
	}
}

func (r *Rock) left() {
	if r.shape[0].X - r.offset > 0 {
		for _, s := range r.shape {
			s.X -= 1
		}
	}
}

func (r *Rock) right() {
	if r.shape[0].X + r.rOffset < XBOUND - 1 {
		for _, s := range r.shape {
			s.X += 1
		}
	}
}

func (r *Rock) move(to *YX) {
	xDist := to.X - r.shape[0].X
	yDist := to.Y - r.shape[0].Y

	for _, s := range r.shape {
		s.Y += yDist
		s.X += xDist
	}
}

func (r *Rock) intersectsRight(c *map[YX]bool) bool {
	for _, s := range r.shape {
		if (*c)[YX{s.Y, s.X+1}] {
			return true
		}
	}
	return false
}

func (r *Rock) intersectsLeft(c *map[YX]bool) bool {
	for _, s := range r.shape {
		if (*c)[YX{s.Y, s.X-1}] {
			return true
		}
	}
	return false
}

func (r *Rock) intersectsBelow(c *map[YX]bool) bool {
	for _, s := range r.shape {
		if (*c)[YX{s.Y-1, s.X}] {
			return true
		}
	}
	return false
}

func (r *Rock) topR() *YX {
	return r.shape[0]
}

func setRock(c *map[YX]bool, rock *Rock) {
	for i := 0; i < len(rock.shape); i++ {
		(*c)[*rock.shape[i]] = true
	}
}

func display(c *map[YX]bool, Ybound int, rocks ...*Rock) {
	b := strings.Builder{}
	shapeCoords := make(map[YX]bool)

	for i := 0; i < len(rocks); i++ {
		rock := rocks[i]
		for j := 0; j < len(rock.shape); j++ {
			shapeCoords[*rock.shape[j]] = true
		}
	}

	for y := Ybound; y >= 0; y-- {
		b.WriteString("|")
		for x := 0; x < XBOUND; x++ {
			p := YX{y, x}
			if (*c)[p] && shapeCoords[p] {
				b.WriteString("X")
			} else if (*c)[p] {
				b.WriteString("#")
			} else if shapeCoords[p] {
				b.WriteString("@")
			} else {
				b.WriteString(".")
			}
		}
		b.WriteString("|\n")
	}
	fmt.Println(b.String())
}

func initialTopR(rock *Rock, maxY int) *YX {
	return &YX{maxY + rock.height + 3, rock.offset + 2}
}

func main() {
	jetPattern, err := os.ReadFile("inp.txt")
	u.Must(err)
	chamber := make(map[YX]bool)
	for x := 0; x < XBOUND; x++ {
		chamber[YX{0, x}] = true
	}

	height := 0
	jetSize := len(jetPattern)
	var rock *Rock
	var topR *YX
	i := 0
	j := 0
	num := 2022
	for {
		rock = create(allKinds[i], &YX{})
		topR = initialTopR(rock, height)
		rock.move(topR)

		for {
			dir := jetPattern[j]
			if dir == LEFT && !rock.intersectsLeft(&chamber) {
				rock.left()
			} else if dir == RIGHT && !rock.intersectsRight(&chamber) {
				rock.right()
			}
			j++
			j%=jetSize

			if rock.intersectsBelow(&chamber) {
				setRock(&chamber, rock)
				height = u.Max(height, rock.topR().Y)
				num--
				break
			} else {
				rock.down()
			}

		}
		if num == 0 {
			fmt.Println(height)
			break
		}

		i++
		i%=5
	}
	fmt.Println((1000000000000 - 1732) / 1735 * 2673 + 2649 + 227)
}