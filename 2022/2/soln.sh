#!/bin/bash
DIR=$(cd `dirname $0` && pwd)
INFL=$DIR/inp2.txt

declare -A scoring=("AX" 4 "AY" 8 "AZ" 3 "BX" 1 "BY" 5 "BZ" 9 "CX" 7 "CY" 2 "CZ" 6)
declare -A reactions=("AX" "AZ" "AY" "AX" "AZ" "AY" "BX" "BX" "BY" "BY" "BZ" "BZ" "CX" "CY" "CY" "CZ" "CZ" "CX")
declare -i score=0
declare -i score2=0

while read line;
 do
	key=$(echo $line | tr -d ' ')
	let score=$score+${scoring[$key]}
	key=${reactions[$key]}
	let score2=$score2+${scoring[$key]}

done < $INFL
# 1 redirecting stdin of a complete while-loop wille xecute in this shell
# 2 redirecting stdin into the while predicate (i.e. "while (predicate) < $FL")
#   will only execute the predicate once (i.e. the same line reads over and over)
# 3 piping stdout into while stdin works the same as (1) but it will execute in a subshell


echo -e "1: $score\n2: $score2"
