#!/bin/bash

# FUNCNAME is an indexed array representing the callstack with the current
# function-scope at 0

abspath() {
	# get the absolute path to the given file
	# Note: `dirname $(abspath <file>)` gives the abspath to the dir
	if [ -z "$1" ]; then
		echo "``USAGE: ${FUNCNAME[0]}  <fname>``"
		return
	fi
	
	# Parameter expansion with longest matching prefix
	echo "$(cd `dirname $1` && pwd)/${1##*/}"
	
}

fhtoarr() {
	# Read the given file into an indexed array line by line
	# array is called `arr`
	if [ -z "$1" ]; then
		echo "``USAGE: ${FUNCNAME[0]} <fname>``"
		return
	fi
	# The explicitly passed delimiter is superfluous (it's the defautlt)
	# but serves as an example of ANSI-C quoting and a reminder of this
	# option. The same goes for the filedescriptor option -u (stdin is the default)
	mapfile -d $'\n' -u 0 arr < $1
}

chr() {
  [ "$1" -lt 256 ] || return 1
  printf "\\$(printf '%03o' "$1")"
}

ord() {
  LC_CTYPE=C printf '%d' "'$1"
}
