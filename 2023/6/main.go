package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var rgx = regexp.MustCompile(`\d+`)
var rgx2 = regexp.MustCompile(`\d`)

func strtoint(e string) int {
	i, err := strconv.ParseInt(e, 10, 64)
	check(err)
	return int(i)
}

func map_(f func(string) int, arr []string) []int {
	r := make([]int, 0)
	for _, s := range arr {
		r = append(r, f(s))
	}
	return r
}

func check(e error) {
	if e != nil {
		panic(e)
	}
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

	lines := strings.Split(string(data), "\n")
	races := make([][2]int, len(rgx.FindAllString(lines[0], -1)))

	big_race := [2]int{0, 0}
	for j, line := range lines {
		nmbrs := map_(strtoint, rgx.FindAllString(line, -1))
		for i := 0; i < len(nmbrs); i++ {
			races[i][j] = nmbrs[i]
		}
		nmbrs = map_(strtoint, rgx2.FindAllString(line, -1))
		exp := len(nmbrs)
		for i := 0; i < exp; i++ {
			big_race[j] += nmbrs[i] * int(math.Pow(10, float64(exp-1-i)))
		}
	}

	res := 1

	for i := 0; i < len(races); i++ {
		time, dist := races[i][0], races[i][1]
		res *= raceResult(time, dist)
	}
	fmt.Println(res)
	fmt.Println(raceResult(big_race[0], big_race[1]))
	fmt.Println(big_race)

	// It is also possible to find all integer solutions to x^2 - tx + r < 0

	t, r := big_race[0], big_race[1]
	left_solution := int((float64(t) + math.Sqrt(-4.0*float64(r)+math.Pow(float64(t), 2))) / 2)
	right_solution := int((float64(t) - math.Sqrt(-4.0*float64(r)+math.Pow(float64(t), 2))) / 2)
	min_solution := math.Min(float64(left_solution), float64(right_solution))
	max_solution := math.Max(float64(left_solution), float64(right_solution))
	fmt.Println(int(math.Floor(max_solution) - math.Ceil(min_solution)))

}

func raceResult(time int, dist int) int {
	threshold := 0
	delta := 1
	for {
		threshold += (time - delta)
		if dist < threshold {
			return (time - delta)
		}
		delta += 2
		if time-delta < 0 {
			return 1
		}
	}
}
