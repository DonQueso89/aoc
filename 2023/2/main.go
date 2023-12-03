package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func flatten(arr [][]string) []string {
	res := make([]string, 0)
	for _, e := range arr {
		res = append(res, e...)
	}
	return res
}

func possible(games []string) (bool, int64) {
	p := true
	m := make([]int64, 3)
	for _, game := range games {
		for _, entry := range strings.Split(game, ",") {
			def := strings.Split(strings.TrimSpace(entry), " ")
			n, clr := def[0], def[1]
			i, err := strconv.ParseInt(n, 10, 8)
			check(err)

			switch {
			case i > 12 && clr == "red":
				p = false
			case i > 13 && clr == "green":
				p = false
			case i > 14 && clr == "blue":
				p = false
			}
			switch clr {
			case "red":
				m[0] = max(i, m[0])
			case "green":
				m[1] = max(i, m[1])
			case "blue":
				m[2] = max(i, m[2])

			}
		}

	}
	return p, m[0] * m[1] * m[2]
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

	var s int64 = 0
	var s2 int64 = 0
	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		prefix := strings.Split(line, ":")
		id, err := strconv.ParseInt(strings.Split(prefix[0], " ")[1], 10, 8)
		check(err)
		games := strings.Split(prefix[1], ";")
		possible_, power := possible(games)
		if possible_ {
			s += id
		}
		s2 += power
	}
	fmt.Println(s)
	fmt.Println(s2)
}
