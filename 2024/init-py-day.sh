#!/usr/bin/zsh
#

if [ -z $1 ]; then echo "Usage: $0 <dirname: int>"; exit 1; fi

if [ -d $1 ]; then 
        echo "Directory for day $1 already exists. Overwrite? y/n"
        read INP
        if [ $INP != "y" ]; then exit; fi
        rm -rf $1
fi

mkdir $1 && cp _template.py $1/main.py && xclip -o > $1/in && chmod +x $1/main.py