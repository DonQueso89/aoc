#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

solve() {
	local numknots=$1
	local -A visited
	local -A knots
	for i in `seq 0 $(( $numknots - 1 ))`; do
		knots["$i 0"]=0
		knots["$i 1"]=0
	done
	while read line;
		do 
			local d=${line:0:1}
			local s=${line:2}
			case $d in
				R) idx=1; m=1;;
				L) idx=1; m=-1;;
				U) idx=0; m=1;;
				D) idx=0; m=-1;;
			esac
			until [ $s -eq 0 ]; do
				let knots["0 $idx"]+=$m
				for k in `seq 1 $(( $numknots - 1 ))`; do
					local h=(${knots["$(( $k - 1 )) 0"]} ${knots["$(( $k - 1 )) 1"]})
					local t=(${knots["$k 0"]} ${knots["$k 1"]})
					local delta=($(( ${h[0]} - ${t[0]} )) $(( ${h[1]} - ${t[1]} )))
					case "${delta[@]}" in
						"2 0") let t[0]+=1;;
						"2 2") let t[0]+=1; let t[1]+=1;;
						"-2 -2") let t[0]-=1; let t[1]-=1;;
						"2 -2") let t[0]+=1; let t[1]-=1;;
						"-2 2") let t[0]-=1; let t[1]+=1;;
						"0 2") let t[1]+=1;;
						"0 -2") let t[1]-=1;;
						"-2 0") let t[0]-=1;;
						"2 1"|"1 2") let t[0]+=1; let t[1]+=1;;
						"-2 -1"|"-1 -2") let t[0]-=1; let t[1]-=1;;
						"-2 1"|"-1 2") let t[0]-=1; let t[1]+=1;;
						"1 -2"|"2 -1") let t[0]+=1; let t[1]-=1;;
					esac
					knots["$k 0"]=${t[0]}
					knots["$k 1"]=${t[1]}
					if [ $k -eq $(( $numknots - 1)) ]; then
						visited["${t[0]},${t[1]}"]=
					fi
				done
				let s--
			done
	done < $INFL
	echo ${#visited[@]};
}

solve 2
solve 10
