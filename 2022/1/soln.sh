#!/bin/bash
DIR=$(cd `dirname $0` && pwd)
INFL=$DIR/inp1.txt

declare -i cur=0
declare -a l
declare -i count=0 
while read line;
 do
 if [ -n "$line" ]; then
    let cur=$cur+$line
 fi
 if [ -z "$line" ]; then
    l[$count]=$cur
    let cur=0
    let count++
 fi

done < $INFL

largest=($(IFS=$'\n'; echo "${l[*]}" | sort -g | tail -n3))
echo "1: ${largest[2]}"
echo "2: $((${largest[2]} + ${largest[1]} + ${largest[0]}))"