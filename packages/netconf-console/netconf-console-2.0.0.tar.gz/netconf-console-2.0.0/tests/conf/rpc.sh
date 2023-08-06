#!/bin/bash

i=''
if  [ $# -gt 1 ]
then
    i=$2
fi

echo a $i
echo b ${#i}
