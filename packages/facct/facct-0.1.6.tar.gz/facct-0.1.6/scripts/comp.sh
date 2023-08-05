#!/bin/bash
if [ ! $# -eq 2 ]; then
    echo "Please give two files as inputs" >&2
    exit 2
fi
f1=$1
f2=$2
if [ ! -f "$f1" ]; then
    echo "$f1: no such file" >&2
    exit 2
fi
if [ ! -f "$f2" ]; then
    echo "$f2 no such file" >&2
    exit 2
fi

cut -d',' -f2- < $f1 >$f1.new
cut -d',' -f2- < $f2 >$f2.new
diff -b $f1.new $f2.new
