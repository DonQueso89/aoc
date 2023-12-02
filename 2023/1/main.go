package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
	"unicode"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func hasPrefix(s string) (bool, int) {
	if strings.HasPrefix(s, "one") {
		return true, 1
	}
	if strings.HasPrefix(s, "two") {
		return true, 2
	}
	if strings.HasPrefix(s, "three") {
		return true, 3
	}
	if strings.HasPrefix(s, "four") {
		return true, 4
	}
	if strings.HasPrefix(s, "five") {
		return true, 5
	}
	if strings.HasPrefix(s, "six") {
		return true, 6
	}
	if strings.HasPrefix(s, "seven") {
		return true, 7
	}
	if strings.HasPrefix(s, "eight") {
		return true, 8
	}
	if strings.HasPrefix(s, "nine") {
		return true, 9
	}
	if strings.HasPrefix(s, "zero") {
		return true, 0
	}
	return false, 0
}

func score(line string) (int, int) {
	s := 0
	s2 := 0
	mult := 10
	mult2 := 10
	value := 0
	value2 := 0
	for i, r := range line {
		if unicode.IsDigit(r) {
			value = int(r - '0')
			s += value * mult
			mult = 0

			value2 = int(r - '0')
			s2 += value2 * mult2
			mult2 = 0
		}

		isNum, n := hasPrefix(line[i:])

		if isNum {
			value2 = n
			s2 += value2 * mult2
			mult2 = 0
		}

	}
	s += value
	s2 += value2
	return s, s2
}

func main() {
	var testing bool
	flag.BoolVar(&testing, "test", false, "--test  to Run with test input")
	flag.Parse()
	fname := "in"
	if testing {
		fname = "test"
	}

	data, err := os.ReadFile(fname)
	check(err)
	lines := strings.Split(string(data), "\n")

	s := 0
	s2 := 0
	for _, line := range lines {
		d1, d2 := score(line)
		s += d1
		s2 += d2

	}
	fmt.Println(s)
	fmt.Println(s2)

}
