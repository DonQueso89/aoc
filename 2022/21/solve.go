package main

import (
	u "aoc/utils"
	"fmt"
	re "regexp"
	"strconv"
	"strings"
)

const ROOT = "root"

type Fraction = u.Fraction

func operator(op string, left, right int64) int64 {
	switch op {
	case "+":
		return left + right
	case "-":
		return left - right
	case "*":
		return left * right
	case "/":
		return left / right
	default:
		return -1
	}
}

func reverseOperator(op string, left, right *Fraction) *Fraction {
	switch op {
	case "+":
		return left.Subtract(right)
	case "-":
		return left.Add(right)
	case "*":
		return left.Divide(right)
	case "/":
		return left.Multiply(right)
	default:
		return &Fraction{0, 0}
	}
}

func resolve(var_ string, legend *map[string][]string) int64 {
	value := (*legend)[var_]
	if len(value) == 1 {
		i, ok := strconv.ParseInt(value[0], 10, 64)
		u.Must(ok)
		return int64(i)
	}
	left, op, right := value[0], value[1], value[2]
	return operator(op, resolve(left, legend), resolve(right, legend))
}

var num = re.MustCompile(`^[0-9]+$`)

func resolveEquation(var_ string, legend *map[string][]string) string {
	value := (*legend)[var_]
	if len(value) == 1 {
		return value[0]
	}
	left, op, right := resolveEquation(value[0], legend), value[1], resolveEquation(value[2], legend)
	if num.MatchString(left) && num.MatchString(right) {
		l, ok := strconv.ParseInt(left, 10, 64)
		u.Must(ok)
		r, ok := strconv.ParseInt(right, 10, 64)
		u.Must(ok)
		return fmt.Sprint(operator(op, int64(l), int64(r)))
	}

	return fmt.Sprintf("(%s %s %s)", left, op, right)

}

func rootSatisfied(humn int64, legend map[string][]string) bool {
	legend["humn"] = []string{fmt.Sprint(humn)}
	left, right := legend[ROOT][0], legend[ROOT][2]
	return resolve(left, &legend) == resolve(right, &legend)
}

var constantOnTheRight = re.MustCompile(`^\(([^0-9]{1}.*) ([-+/*]{1}) ([0-9]+)\)$`)
var constantOnTheLeft = re.MustCompile(`^\(([0-9]+) ([-+/*]{1}) (.*[^0-9]{1})\)$`)

func solveEquation(expression string, numerical *Fraction) *Fraction {
	if expression == "X" {
		return numerical
	}
	var op, constant string
	if constantOnTheRight.MatchString(expression) {
		parts := constantOnTheRight.FindStringSubmatch(expression)
		expression, op, constant = parts[1], parts[2], parts[3]
	} else if constantOnTheLeft.MatchString(expression) {
		parts := constantOnTheLeft.FindStringSubmatch(expression)
		expression, op, constant = parts[3], parts[2], parts[1]

		// some extra transformation when the expression is the right operand
		if op == "-" {
			// a - b = c -> b - a = -c
			numerical = numerical.Multiply(&Fraction{-1, 1})
		} else if op == "/" {
			// a / b = c -> a / c = b
			numerical = numerical.Reciprocal()
			op = "*"
		}
	}

	parsedConstant, ok := strconv.ParseInt(constant, 10, 64)
	u.Must(ok)

	return solveEquation(expression, reverseOperator(op, numerical, &Fraction{int64(parsedConstant), 1}))
}

func main() {
	lines := u.ReadLines(u.GetInputFile())
	legend := make(map[string][]string)

	for _, line := range lines {
		if len(line) == 0 {
			continue
		}
		payload := strings.Split(line, " ")
		legend[strings.Trim(payload[0], ":")] = payload[1:]
	}

	fmt.Println(resolve(ROOT, &legend))
	legend["humn"] = []string{"X"}
	legend[ROOT][1] = "="
	equationString := resolveEquation(ROOT, &legend)
	equation := strings.Split(equationString[1:len(equationString)-1], " = ")
	numerical, ok := strconv.ParseInt(equation[1], 10, 64)
	u.Must(ok)
	solution := solveEquation(equation[0], &Fraction{N: int64(numerical), D: 1})
	fmt.Println(solution)
	fmt.Println(rootSatisfied(solution.Int(), legend))
}
