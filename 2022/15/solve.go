package main

import (
	u "aoc/utils"
	"fmt"
	"math"
	"os"
	re "regexp"
	"strconv"
	"strings"
	"sort"
)

type YX struct {
	y int
	x int
}

func (a *YX) Dist(b *YX) int {
	return int(math.Abs(float64(a.y-b.y)) + math.Abs(float64(a.x-b.x)))
}

type Sensor struct {
	pos    *YX
	beacon *YX
}

func (s *Sensor) Dist() int {
	return s.pos.Dist(s.beacon)
}

func (s *Sensor) String() string {
	return fmt.Sprintf("<S: (y=%d, x=%d) B: (y=%d, x=%d)>", s.pos.y, s.pos.x, s.beacon.y, s.beacon.x)
}

func max(n ...int) int {
	r := n[0]
	for i := 1; i < len(n); i++ {
		e := n[i]
		if e > r {
			r = e
		}
	}
	return r
}
func min(n ...int) int {
	r := n[0]
	for i := 1; i < len(n); i++ {
		e := n[i]
		if e < r {
			r = e
		}
	}
	return r
}

func numExcluded(Y int, beacons map[YX]bool, sensors []*Sensor, lowerBound int, upperBound int, excludeBeacons bool) (int, YX) {
	ranges := make([][2]int, 0)
	var minX, maxX int
	gaps := 0
	done := make(map[YX]bool)

	for i := 0; i < len(sensors); i++ {
		sensor := sensors[i]
		beaconDist := sensor.Dist()
		yDist := int(math.Abs(float64(Y - sensor.pos.y)))

		if yDist > beaconDist {
			continue
		}

		offset := beaconDist - yDist
		lb := (sensor.pos.x - offset)
		ub := (sensor.pos.x + offset)

		if lowerBound != -1 {
			lb = max(lowerBound, lb)
		}
		if upperBound != -1 {
			ub = min(upperBound, ub)
		}

		for beacon, _ := range(beacons) {
			if !done[beacon] && excludeBeacons && beacon.y == Y && lb <= beacon.x && beacon.x <= ub {
				gaps++
				done[beacon] = true
			}
		}

		ranges = append(ranges, [2]int{lb, ub})
		if ub > maxX {
			maxX = ub
		}
		if lb < minX {
			minX = lb
		}
	}

	sort.Slice(ranges, func(i, j int) bool {
		return ranges[i][0] < ranges[j][0]
	})

	var target YX
	upperBounds := make([]int, 0)

	for i := 1; i < len(ranges); i++ {
		upperBounds = append(upperBounds, ranges[i-1][1])
		r := ranges[i][0]
		gap := r - max(upperBounds...)
		if gap > 1 {
			gaps += (gap - 1)
			target = YX{Y, r - 1}
		}
	}


	return maxX + 1 - minX - gaps, target
}

var patt = re.MustCompile(`[-0-9]+`)

func main() {
	data, err := os.ReadFile("inp.txt")
	u.Must(err)
	lines := strings.Split(string(data), "\n")
	sensors := make([]*Sensor, 0)
	beacons := make(map[YX]bool)
	for _, line := range lines {
		if len(line) == 0 {
			continue
		}

		payload := u.Map[string, int](patt.FindAllString(line, -1), func(s string) int {
			i, _ := strconv.ParseInt(s, 10, 64)
			return int(i)
		})

		beacon := &YX{payload[3], payload[2]}
		beacons[*beacon] = true
		sensors = append(sensors, &Sensor{&YX{payload[1], payload[0]}, beacon})
	}
	
	n, _ := numExcluded(10, beacons, sensors, -1, -1, true)
	fmt.Printf("1: %d\n", n)

	bound := 4000000
	for y := 0; y <= bound;  y++ {
		_, t := numExcluded(y, beacons, sensors, 0, bound, false)
		if t.x > 0 {
			fmt.Printf("2: %d\n", t.x * 4000000 + t.y)
			break
		}
	}
}
