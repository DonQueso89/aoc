#!/usr/bin/zsh
#
if [ -z $1 ]; then echo "Usage: $0 <dirname: int>"; exit 1; fi

if [ -d $1 ]; then 
        echo "Directory for day $1 already exists. Overwrite? y/n"
        read INP
        if [ $INP != "y" ]; then exit; fi
        rm -rf $1
fi

mkdir $1 &&
cd $1 &&
xclip -o > in &&
cat <<EOF > main.go
package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

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
	for _, line := range lines {
                fmt.Println(line)
	}

}
EOF
