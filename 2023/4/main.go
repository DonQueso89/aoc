package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"regexp"
	"slices"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

var rgx = regexp.MustCompile(`\d+`)

func score(winning *[]string, mine *[]string) (s, e int) {
	e--
	for _, n := range *mine {
		if slices.Contains(*winning, n) {
			e++
		}
	}
	if e >= 0 {
		s = int(math.Pow(2, float64(e)))
	}
	return s, e + 1
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

	cards := make([][2][]string, len(lines))
	for i, line := range lines {
		if len(line) == 0 {
			continue
		}
		nmbrs := strings.Split((strings.Split(strings.TrimSpace(line), ":")[1]), "|")
		winning, mine := rgx.FindAllString(nmbrs[0], -1), rgx.FindAllString(nmbrs[1], -1)

		cards[i] = [2][]string{winning, mine}
	}

	s2 := 0
	s := 0
	incr := make([]int, len(cards))
	for j, c := range cards {
		fmt.Println(j)
		w, n := score(&c[0], &c[1])
		fmt.Printf("GAme %d wins %d", j, w)
		s += w
		s2 += (1 + incr[j])

		for i := n; i > 0; i-- {
			incr[j+i] += (1 + incr[j])
		}
		fmt.Println(incr)
	}
	fmt.Println(s)
	fmt.Println(s2)
}
