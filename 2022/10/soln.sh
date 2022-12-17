#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

targets=(20 60 100 140 180 220 260)
shopt -qs extglob

incr() {
	IFS='|'; if [[ $1 == @(${targets[*]}) ]]; then
		echo $(( $1 * $2 ))
	else 
		echo 0
	fi
}

draw() {
	sprite="$(( $2-1 ))|$2|$(( $2+1 ))"
	if [[ $(( ($1 % 40) - 1 )) == @($sprite) ]] ; then
		echo -n '#'
	else
		echo -n "."
	fi
	if [ $(( $1 % 40 )) == 0 ]; then
		echo
	fi

}

c=1
x=1
s=0
while read line;
	do 
		IFS=' '; l=($line)
		draw $c $x
		let s+=$(incr $c $x)
		let c++
		if [ ${l[0]} == "addx" ]; then
			draw $c $x
			let s+=$(incr $c $x)
			let c++
			let x+=${l[1]}
		fi	
done < $INFL
echo $s
