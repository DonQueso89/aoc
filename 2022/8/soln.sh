#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

fhtoarr $INFL

# 99^2*2*98=1920996 comparisons 

maxx=${#arr[@]}
let tot=$(( 4 * ($maxx-1) ))
let maxscenic=0
for y in `seq 1 $(( ${#arr[@]} - 2 ))`;
	do 	
		line=${arr[$y]}
		for x in `seq 1 $(( $maxx - 2 ))`; do
			let scenic=1
			visible=1
			act=1
			t=${line:$x:1}
			xs=(`seq $(( $x - 1 )) -1 0`) 
			for sx in ${xs[@]}; do
				if [ ${line:$sx:1} -ge $t  ]; then
					visible=0
					let scenic*=$(( $x - $sx ))
					break 1
				fi
			done
			let tot+=$visible
			if [[ $visible -eq 1 ]]; then let scenic*=$x; act=0; fi
			visible=1
			xs=(`seq $(( $x + 1 )) $(( $maxx - 1 ))`)
			for sx in ${xs[@]}; do
				if [ ${line:$sx:1} -ge $t  ]; then
					visible=0
					let scenic*=$(( $sx - $x ))
					break 1
				fi
			done
			let tot+=$(( $visible * $act ))
			if [[ $visible -eq 1 ]]; then let scenic*=$(( $maxx - $x - 1 )); act=0; fi
			visible=1
			ys=(`seq $(( $y - 1 )) -1 0`)
			for sy in ${ys[@]}; do
				sline=${arr[$sy]}
				if [ ${sline:$x:1} -ge $t  ]; then
					visible=0
					let scenic*=$(( $y - $sy ))
					break 1
				fi
			done
			let tot+=$(( $visible * $act ))
			if [[ $visible -eq 1 ]]; then let scenic*=$y; act=0; fi
			visible=1
			ys=(`seq $(( $y + 1 )) $(( $maxx - 1 ))`)
			for sy in ${ys[@]}; do
				sline=${arr[$sy]}
				if [ ${sline:$x:1} -ge $t  ]; then
					visible=0
					let scenic*=$(( $sy - $y ))
					break 1
				fi
			done
			let tot+=$(( $visible * $act ))
			if [[ $visible -eq 1 ]]; then let scenic*=$(( $maxx - $y - 1 )); fi
			if [[ $scenic -gt $maxscenic ]]; then
				maxscenic=$scenic
			fi
		done
done
echo $tot
echo $maxscenic
