#!/bin/bash
source /home/kees/aoc/2022/utils.sh

DIR=$(dirname $(abspath $0))
INFL=$DIR/inp.txt
let cnt=0
let cnt2=0
while read line;
	do 
		# the shell scans the result of the parameter expansion
		# for word splitting, so IFS can be used to construct the
		# elements to the array
		IFS="-,"; lh=(${line%%,*})
		IFS="-"; rh=(${line##*,})
		
		# [[ is a compound command, [ is a builtin command with ]
		# the last mandatory operator
		# when [[ is used, the arguments to -le/-ge etc.. 
		# are evaluated as arithmetic expressions

		# every [] block in the conditions section is just
		# an invocation of [ separated by the && control operator
		if [ ${lh[0]} -le ${rh[0]} ] && [ ${lh[1]} -ge ${rh[1]} ]; then
			let cnt++
		elif [ ${rh[0]} -le ${lh[0]} ] && [ ${rh[1]} -ge ${lh[1]} ]; then
			let cnt++
		fi

		if [ ${lh[1]} -lt ${rh[0]} ] || [ ${rh[1]} -lt ${lh[0]} ]; then
			continue
		else
			let cnt2++
		fi
done < $INFL

echo "1: $cnt 2: $cnt2"

