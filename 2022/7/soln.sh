#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

declare -a stack
declare -A sizes
while read line; do	
		case $line in
	  	  \$?cd?..)
			  stack=(${stack[@]:0:$(( ${#stack[@]} - 1 ))})
		  ;;
		  \$?cd*) 
			  stack+=(${line##\$ cd })
		  ;;
		  \$?ls) 
			  continue
		  ;;
		  *)
			  value=${line%%[^0-9]*}
			  for i in `seq 0 $(( ${#stack[@]} - 1 ))`; do
				  fldr=${stack[$i]}
				  ident="$(echo ${stack[@]:0:$i} | tr -d ' ')"
				  let sizes["$fldr-$ident"]+=${value:-0}
			  done
		  ;;
	  	esac
done < $INFL

res=0
let free_=$(( 70000000 - ${sizes[/-]} ))
echo "free: $free_"
min=30000000
for f in ${!sizes[@]}; do
	v=${sizes[$f]}
	if [ $v -le 100000 ]; then
		let res+=$v
	fi

	if [[ $(( $free_ + $v )) -ge 30000000 ]] && [[ $v -lt $min  ]] ; then
		min=$v	
	fi
done

echo $res
echo $min
