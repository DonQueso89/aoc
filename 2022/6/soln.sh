#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

read in_ < $INFL

detect() {
	line=$1
	size=$2
	len=${#line}
	for i in `seq 0 $(( $len - $size ))`; do
		declare -A d
		s="${line:$i:$size}"
		for j in `seq 0 $(( $size - 1))`; do
			d[${s:$j:1}]=''
		done

		keys=(${!d[@]})
		if [ ${#keys[@]} -eq $size ]; then
			echo $(( i + $size ));
			break;
		fi
		unset d
	done
}

detect $in_ 4
detect $in_ 14
