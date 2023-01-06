package main

import u "aoc/utils"
import sc "strconv"
import "os"
import "fmt"
import "strings"
import "sort"

type any = interface{}
type Packet []any
type Pair [2]Packet

const BOPEN = 91
const BCLOSE = 93
const COMMA = 44
const ZERO = 48
const ONE = 49
const EQUAL = 0
const ORDERED = 1
const UNORDERED = 2

func cmpInt(l int, r int) int {
	if l < r {
		return ORDERED
	} else if l > r {
		return UNORDERED
	}
	return EQUAL
}
func cmpArr(a Packet, b Packet) int {
	var result int
	for idx := 0; idx < len(a); idx++ {
		if idx == len(b) {
			return UNORDERED
		}
		ea := a[idx]
		eb := b[idx]
		at, aIsInt := ea.(int)
		bt, bIsInt := eb.(int)

		if aIsInt && bIsInt {
			result = cmpInt(at, bt)
		} else if aIsInt {
			eb := eb.(Packet)
			result = cmpArr(Packet{ea}, eb)
		} else if bIsInt {
			ea := ea.(Packet)
			result = cmpArr(ea, Packet{eb})
		} else {
			eb := eb.(Packet)
			ea := ea.(Packet)
			result = cmpArr(ea, eb)
		}

		if result == EQUAL {
			continue
		}
		return result
	}
	if len(b) > len(a) {
		return ORDERED
	}
	return EQUAL
}

func evaluate(p Pair) int {
	return cmpArr(p[0], p[1])
}

func main() {
	data, err := os.ReadFile("inp.txt")
	u.Must(err)
	lines := strings.Split(string(data), "\n")

	var stack []Packet
	var cur Packet
	var pairs = make([]Pair, 0)
	pair := Pair{}
	packets := []Packet{
		Packet{Packet{2}},
		Packet{Packet{6}},
	}
	idx := 0
	for _, line := range lines {
		if len(line) == 0 {
			pairs = append(pairs, pair)
			packets = append(packets, pair[0], pair[1])
			pair = Pair{}
			idx = 0
			continue
		}
		cur = nil
		stack = make([]Packet, 0)
		for idx, s := range line {
			switch s {
				case BOPEN:
					if cur != nil {
						stack = append(stack, cur)
					}
					cur = make(Packet, 0)
				case BCLOSE:
					if len(stack) > 0 {
						parent := stack[len(stack) - 1]
						parent = append(parent, cur)
						cur = parent
						stack = stack[:len(stack) - 1]
					}
				case ONE:
					if line[idx + 1] == ZERO {
						cur = append(cur, int(10))
						continue
					}
					cur = append(cur, 1)
				case ZERO:
					if line[idx - 1] == ONE {
						continue
					}
					cur = append(cur, int(0))
				case COMMA:
					continue
				default:
					n, err  := sc.ParseInt(string(s), 10, 8)
					u.Must(err)
					cur = append(cur, int(n))
				}
		}
		pair[idx] = cur
		idx++
	}
	pairs = append(pairs, pair)
	packets = append(packets, pair[0], pair[1])
	s := 0
	for i, p := range pairs {
		if evaluate(p) == ORDERED {
			s+=i
			s++
		}
	}

	fmt.Printf("1: %d\n", s)
	
	sort.Slice(packets, func(i, j int) bool {
		return evaluate(Pair{packets[i], packets[j]}) == ORDERED
	})

	id := 1
	for i, p := range packets {
		if cmpArr(Packet{Packet{2}}, p) == EQUAL || cmpArr(Packet{Packet{6}}, p) == EQUAL {
			id *= (i + 1)
		}
	}
	fmt.Printf("2: %d\n", id)
}