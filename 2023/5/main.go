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

func converterFactory(entries []string) func(int, bool) int {
	defs := make([][3]int, len(entries))
	for _, e := range entries {
		s := map_(strtoint, strings.Split(e, " "))
		defs = append(defs, [3]int{s[0], s[1], s[2]})
	}

	return func(i int, reverse bool) int {
		for idx := 0; idx < len(defs); idx++ {
			entry := defs[idx]
			dst, src, size := entry[0], entry[1], entry[2]
			if reverse {
				src, dst, size = entry[0], entry[1], entry[2]
			}
			if src <= i && i < src+size {
				return dst + (i - src)
			}
		}
		return i
	}
}

func convert(converters []func(int, bool) int, s int, reverse bool) int {
	for idx := 0; idx < len(converters); idx++ {
		c := converters[idx]
		if reverse {
			c = converters[len(converters)-1-idx]
		}
		s = c(s, reverse)
	}
	return s
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
	seeds := make([]int, 0)
	entries := make([]string, 0)
	converters := make([]func(int, bool) int, 0)
	for i, line := range lines {
		if i == 0 {
			for _, e := range strings.Split(line[7:], " ") {
				s, err := strconv.ParseInt(e, 10, 64)
				check(err)
				seeds = append(seeds, int(s))
			}
			continue
		}
		if strings.HasSuffix(line, ":") {
			continue
		}
		if (len(line) == 0 && len(entries) > 0) || i == len(lines)-1 {
			converters = append(converters, converterFactory(entries))
			entries = make([]string, 0)
			continue
		}
		if len(line) > 0 {
			entries = append(entries, line)
		}
	}

	min := 1 << 32
	for _, s := range seeds {
		o := convert(converters, s, false)
		if o < min {
			min = o
		}
	}

	fmt.Println(min)

	mappable := func(n int) bool {
		for i := 0; i < len(seeds); i += 2 {
			if seeds[i] <= n && n < seeds[i]+seeds[i+1] {
				return true
			}
		}
		return false
	}

	l := 0
	for {
		c := convert(converters, l, true)
		if mappable(c) {
			fmt.Println(l)
			break
		}
		l++
	}
}
