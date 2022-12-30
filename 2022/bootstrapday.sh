#!/bin/bash
USAGE="USAGE: ``${FUNCNAME[0]} <name> <day[1,24]>``"
if [ -z "$1" ]; then
	echo $USAGE
	exit
fi

if [[ -z "$2" || $2 -gt 24 || $2 -lt 0  ]]; then
	echo $USAGE
	exit
fi

source utils.sh
DIR=$(dirname $(abspath $0))

# parameter expansion with shortest matching suffix deleted
# from expansion of $1
dirn=${1%.sh}
filen=soln.sh

mkdir $dirn
echo "#!/bin/bash
source $DIR/utils.sh

DIR=\$(dirname \$(abspath \$0))
INFL=\$DIR/inp.txt

while read line;
	do 
		echo \$line
done < \$INFL
" >> $dirn/$filen
chmod +x $dirn/$filen

# expects stdin to be written to
# otherwise blocks
while read inpline; do
	echo "$inpline" >> $dirn/inp.txt
done
echo $inpline >> $dirn/inp.txt
