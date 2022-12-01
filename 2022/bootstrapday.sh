#!/bin/bash

if [ -z "$1" ]; then
	echo "must pass name as first arg"
fi

if [[ -z "$2" || $2 -gt 24 || $2 -lt 0  ]]; then
	echo "must pass day as second arg [1,24]"
fi

# Note the space between : and - to avoid confusion
# with the `:-` expansion
dirn=${1%.sh}
filen=soln.sh

mkdir $dirn
echo '#!/bin/bash' > $dirn/$filen
echo 'DIR=$(cd `dirname $0` && pwd)' >> $dirn/$filen
echo "INFL=\$DIR/inp$2.txt" >> $dirn/$filen
echo -e 'while read line;\n do\n echo $line\n
done < $INFL\n
' >> $dirn/$filen
chmod +x $dirn/$filen

while read inpline; do
	echo $inpline >> $dirn/inp${2}.txt
done
echo $inpline >> $dirn/inp${2}.txt
