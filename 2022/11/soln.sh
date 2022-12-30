#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

while read line;
	do 
		echo $line
done < $INFL

