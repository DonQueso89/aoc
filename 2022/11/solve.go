package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
)

func must(err error) {
	if err != nil {
		log.Fatal("An error occurred", err)
	}
}

type Remainders = map[int]int
type operation = func(int) int
type monkey[T int | *Remainders] func(T) (T, int)

func exp(o int) int {
	return o * o
}

func multFac(c int) operation {
	return func(n int) int {
		return n * c
	}
}
func addFac(c int) operation {
	return func(n int) int {
		return n + c
	}
}

func monkeyFactory(mod int, pass int, fail int, op operation) monkey[int] {
	return func(worry int) (int, int) {
		worry = op(worry) / 3
		if worry % mod == 0 {
			return worry, pass
		}
		return worry, fail

	}
}

func monkeyFactoryR(mod int, pass int, fail int, op operation) monkey[*Remainders] {
	return func(worry *Remainders) (*Remainders, int) {
		for modulus, remainder := range *worry {
			(*worry)[modulus] = op(remainder) % modulus
		}

		if (*worry)[mod] == 0 {
			return worry, pass
		}
		return worry, fail

	}
}

func atoi[T string | []byte](b T) int {
	i, err := strconv.ParseInt(string(b), 10, 8)
	must(err)
	return int(i)
}

func Map[T, R []byte | string | int](a []T, function func(T) R) []R {
	ret := make([]R, len(a))
	for i, e := range a {
		ret[i] = function(e)
	}
	return ret
}

func main() {
	log.SetFlags(0)
	content, err := os.ReadFile("inp.txt")
	must(err)
	lines := bytes.Split(content, []byte("\n"))
	var monkeys [8]monkey[int]
	var monkeysR [8]monkey[*Remainders]
	var bookkeeping [8][]int
	var bookkeepingR [8][]*Remainders
	var counts, countsR [8]int
	var pass, fail, cur, mod int
	var a1, op, a2 string
	var items []int
	var fn operation
	var mods []int
	for _, line := range lines {
		if cap(line) <= 1 {
			continue
		}

		words := bytes.Split(
			bytes.ReplaceAll(
				bytes.TrimLeft(line, " "),
				[]byte(","),
				[]byte(""),
			),
			[]byte{32},
		)

		switch instr, arg := words[0], words[1]; true {
		case bytes.HasPrefix(instr, []byte("Monkey")):
			continue
		case bytes.HasPrefix(instr, []byte("Starting")):
			// type args can also be ommitted and inferred by compiler
			// if the signature of the generic function allows it.
			items = Map[[]byte, int](words[2:], atoi[[]byte])
		case bytes.HasPrefix(instr, []byte("Operation")):
			a1, op, a2 = string(words[3]), string(words[4]), string(words[5])
		case bytes.HasPrefix(instr, []byte("Test")):
			mod = atoi(words[3])
			mods = append(mods, mod)
		case bytes.HasPrefix(instr, []byte("If")) && bytes.HasPrefix(arg, []byte("true")):
			pass = atoi(words[5])
		default:
			fail = atoi(words[5])
			fmt.Printf("%d has mod %v, pass %d fail %d a1 %v a2 %v op %v items %v \n", cur, mod, pass, fail, a1, a2, op, items)
			if a2 == "old" {
				fn = exp
			} else if op == "*" {
				fn = multFac(atoi(a2))
			} else {
				fn = addFac(atoi(a2))
			}
			monkeys[cur] = monkeyFactory(mod, pass, fail, fn)
			monkeysR[cur] = monkeyFactoryR(mod, pass, fail, fn)
			bookkeeping[cur] = items
			cur++
		}
	}

	for k, v := range bookkeeping {
		for _, i := range v {
			remainders := make(Remainders, 0)
			for _, m := range mods {
				remainders[m] = i % m
			}
			bookkeepingR[k] = append(bookkeepingR[k], &remainders)
		}
	}

	for i := 0; i < 20; i++ {
		for n, monkeyfn := range monkeys {
			for _, item := range bookkeeping[n] {
				counts[n]++
				out, tgt := monkeyfn(item)
				bookkeeping[tgt] = append(bookkeeping[tgt], out)
			}
			bookkeeping[n] = make([]int, 0)
		}
	}
	sort.Ints(counts[:])
	fmt.Println(counts)
	fmt.Println(counts[7] * counts[6])

	for i := 0; i < 10000; i++ {
		for n, monkeyfn := range monkeysR {
			for _, item := range bookkeepingR[n] {
				countsR[n]++
				out, tgt := monkeyfn(item)
				bookkeepingR[tgt] = append(bookkeepingR[tgt], out)
			}
			bookkeepingR[n] = make([]*Remainders, 0)
		}
	}
	sort.Ints(countsR[:])
	fmt.Println(countsR)
	fmt.Println(countsR[7] * countsR[6])
}