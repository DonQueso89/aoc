package utils

import (
	"fmt"
	"strings"
	"log"
)

type Numerical interface {
	AddZero()
	Add(*Number) *Number
	Len() int
	Mult(*Number) *Number
	Div(*Number) (*Number, *Number)
	Gte(*Number) bool
	Lte(*Number) bool
	Equals(*Number) bool
	Int() int
}

type Number struct {
	coef []int
}

func Num(i int) *Number {
	n := Number{make([]int, 0)}
	for e := 0; i > 0; e++ {
		r := i % 10
		i -= r
		i /= 10
		n.AddZero()
		n.coef[e] = r
	}
	return &n
}

func (n *Number) AddZero() {
	// When methods with pointer-receivers are called
	// on values, Go will still call the method with the
	// pointer receiver.
	// i.e., if n is a value: n.AddZero() is the same as (&n).AddZero()
	// This also works the other  way around for methods with
	// value-receivers.
	n.coef = append(n.coef, 0)
}

func (n *Number) Len() int {
	if n == nil {
		return 0
	}
	return len(n.coef)
}

func (n *Number) Add(o *Number) *Number {
	left := n
	right := o
	if o.Len() > n.Len() {
		left = o
		right = n
	}

	var result = &Number{make([]int, 0)}
	keep := 0
	for exp, c := range left.coef {
		s := c + keep
		if exp < right.Len() {
			s += right.coef[exp]
		}
		r := s % 10
		s -= r
		s /= 10
		if exp >= result.Len() {
			result.AddZero()
		}
		result.coef[exp] += r
		keep = s
	}

	if keep > 0 {
		result.AddZero()
		result.coef[len(result.coef)-1] = keep
	}
	return result.Trim()
}

func (n *Number) Mult(o *Number) *Number {
	var result = &Number{make([]int, 0)}
	for ea, a := range n.coef {
		for eb, b := range o.coef {
			p := a * b
			exp := ea + eb
			if exp >= result.Len() {
				result.AddZero()
			}
			p += result.coef[exp]
			result.coef[exp] = 0
			for e := exp; p > 0; e++ {
				r := p % 10
				p -= r
				p /= 10
				if e >= result.Len() {
					result.AddZero()
				}
				result.coef[e] += r
			}
		}
	}
	return result.Trim()
}

func (a *Number) Gte(b *Number) bool {
	// true if a >= b
	al, bl := a.Len(), b.Len()
	fmt.Printf("%v (len: %d) >= %d (len: %d) = %v ",a.coef, a.Len(), b.Int(), b.Len(), a.Int() >= b.Int())
	if al > bl {
		fmt.Printf("true 1\n")
		return true
	} else if al < bl {
		fmt.Printf("false 2\n")
		return false
	} else {
		for i := al - 1; i >= 0; i-- {
			if a.coef[i] == b.coef[i] {
				continue
			} else if a.coef[i] > b.coef[i] {
				fmt.Printf("true 3\n")
				return true
			}
			fmt.Printf("false 4\n")
			return false
		}
	}
	fmt.Printf("true 5\n")
	return true
}

func (a *Number) Equals(b *Number) bool {
	if a.Len() != b.Len() {
		return false
	}

	for i := 0; i < a.Len(); i++ {
		if a.coef[i] != b.coef[i] {
			return false
		}
	}
	return true
}

func (a *Number) Lte(b *Number) bool {
	// true if a <= b
	return a.Equals(b) || !a.Gte(b)
}

func (a *Number) Lt(b *Number) bool {
	// true if a < b
	return !a.Gte(b)
}

func (n *Number) Int() int {
	r := 0
	e := 1
	for i := 0; i < n.Len(); i++ {
		r += n.coef[i] * e
		e *= 10
	}
	return r
}

func (n Number) Div(d *Number) (*Number, *Number) {
	// long division
	n.Trim()
	if n.Equals(Num(0)) {
		return Num(0), Num(0)
	}

	quotient := &Number{make([]int, n.Len())}
	l_exp, r_exp := n.Len(), n.Len()-1
	remainder := &n
	var q, r *Number
	di := d.Int()
	for remainder.Gte(d) {
		cur := &Number{make([]int, 0)}
		for i := r_exp; i < l_exp; i++ {
			cur.coef = append(cur.coef, remainder.coef[i])
		}

		if cur.Lt(d) {
			r_exp--
			continue
		}

		c := cur.Int()
		q, r = Num(c/di), Num(c%di)

		for i := 0; i < q.Len(); i++ {
			quotient.coef[r_exp+i] += q.coef[i]
		}

		for i := 0; i < r.Len(); i++ {
			remainder.coef[r_exp+i] = r.coef[i]
		}

		l_exp = r_exp + r.Len()
		remainder.coef = remainder.coef[:l_exp]
		//fmt.Printf("quotient %v (len: %d) remainder %v (len: %d) remainder > d = %v len d: %d d: %v\n", quotient, quotient.Len(), remainder, remainder.Len(), remainder.Gte(d), d.Len(), d)
	}


	return quotient.Trim(), remainder.Trim()
}

func (n *Number) Trim() *Number {
	var i int
	for i = n.Len() ;i > 0; i-- {
		if n.coef[i-1] > 0 {
			break
		}
	}
	n.coef = n.coef[:i]
	if n.Len() == 0 {
		n.coef = []int{0}
	}
	return n
}

func (n *Number) String() string {
	// implements Stringer interface from fmt
	leadingzero := true
	s := strings.Builder{}
	for exp := n.Len() - 1; exp >= 0; exp-- {
		c := n.coef[exp]
		if c > 0 {
			leadingzero = false
		}

		if !leadingzero {
			s.WriteString(fmt.Sprintf("%d", c))
		}
	}

	if leadingzero {
		return "0"
	}
	return s.String()
}


func Must(err error) {
	if err != nil {
		log.Fatal("An error occurred", err)
	}
}

func Map[T, R int | string | byte](slice []T, fn func(T) R) []R {
	out := make([]R, len(slice))
	for i, e := range slice {
		out[i] = fn(e)
	}
	return out
}

func example() {
	var in Numerical = Num(123)
	var io Numerical = Num(987)
	n := in.(*Number)
	o := io.(*Number)
	fmt.Println(n.Mult(o))
	fmt.Println(n.Add(o))

	fmt.Printf("%d %d %d %d \n", n.Int(), o.Int(), Num(0).Int(), Num(1).Int())

	fmt.Println(n.Div(Num(1)))
	fmt.Println(n.Div(o))
	fmt.Println(o.Div(n))

	fmt.Println(Num(872364).Div(Num(9763)))
}
