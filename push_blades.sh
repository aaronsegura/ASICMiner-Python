#!/bin/sh

BLADEFILE=~/.blades
BLADES=`cat $BLADEFILE`

if [ ! "$1" ]; then
  echo "Must pass desired server:port"
  exit
fi

awkstr="(\$2 !~ \"/$1/\") && (\$2 ~ /^[0-9]/) { print \$1 }"

echo "Probing blades..."
WRONG=`/usr/bin/python ./bm.py $BLADES | awk "$awkstr" | tr -d ']['`

if [ "$WRONG" ]; then
  /usr/bin/python ./bm.py -S $WRONG
fi
