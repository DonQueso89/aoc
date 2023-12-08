package utils

func Strtoint(e string) int {
	i, err := strconv.ParseInt(e, 10, 64)
	check(err)
	return int(i)
}

func Map(f func(string) int, arr []string) []int {
	r := make([]int, 0)
	for _, s := range arr {
		r = append(r, f(s))
	}
	return r
}
