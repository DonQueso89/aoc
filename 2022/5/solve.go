package main

import (
    "fmt"
    "log"
    "os"
    "bytes"
    "strconv"
)

func must(err error){
    if err != nil {
        log.Fatal("An error occurred", err)
    }
}

func reverse(arr []byte) (r []byte) {
    for i := len(arr) - 1; i >= 0; i-- {
        r = append(r, arr[i])
    }
    return
}

func noop(arr []byte) []byte {
    return arr
}

// byte is just an alias for uint8
// rune is an alias for uint32 and represents a Unicode code point
func solve(rev bool) {
    log.SetFlags(0)
    content, err := os.ReadFile("in.txt") // type inference assignment
    must(err)

    reorder := noop
    if rev {
        reorder = reverse
    }

    lines := bytes.Split(content, []byte("\n"))
    stacks := make([][]byte, 9)
    parse := false
    for _, line := range lines {
        if len(line) == 0 { continue }
        if parse {
            parsed := bytes.Split(line, []byte{32})
            num, err := strconv.ParseInt(string(parsed[1]), 10, 8)
            must(err)
            src, err := strconv.ParseInt(string(parsed[3]), 10, 8)
            must(err)
            tgt, err := strconv.ParseInt(string(parsed[5]), 10, 8)
            src--; tgt--;
            offset := len(stacks[src]) - int(num)
            stacks[tgt] = append(stacks[tgt], reorder(stacks[src][offset:])...)
            stacks[src] = stacks[src][:offset]
            continue
        }
        if  string(line[1]) == "1" {
            for j, s := range stacks {
                stacks[j] = reverse(s)
            }
            parse = true
            continue
        }
        for i := 0; i < 9; i++ {
            b := line[1+4*i]
            if b > 32 {
                stacks[i] = append(stacks[i], b)
            }
        }
    }

    for _, s := range stacks {
        fmt.Print(string(s[len(s)-1]))
    }
    fmt.Println()
}

func main() {
    solve(true)
    solve(false)
}
