#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt

OFFSET=38
offset=96

priority() {
	# double brackets allows for pattern matching
	# in conditional constructs
	payload=$1
	if [[ ${payload[0]} == [A-Z]* ]]; then
		echo $(( `ord ${payload[0]}` - $OFFSET ))
	else
		echo $(( `ord ${payload[0]}` - $offset ))
	fi
}

declare -i res
while read line;
	do 
		len=$(( ${#line} / 2 ))
		# substring expansion (${word:offset:length})
		rh=${line:$len}
		lh=${line::$len}
		# -c option uses the complement of the given set
		common=$(echo $lh | tr -cd $rh)
		let res+=$(priority $common)
		
done < $INFL

echo "1: $res"

let res=0
fhtoarr $INFL
len=${#arr[@]}
i=0

# doing substring expansion on indexed arrays
# requires the '@' subscript
until [ $i -eq $len ]; do
	slice=(${arr[@]:$i:3})
	common=$((tr -cd ${slice[1]} | tr -cd ${slice[2]}) < <(echo ${slice[0]}))
	let res+=$(priority $common)
	let i+=3
done

echo "2: $res"
