#!/bin/bash
ROOT=$(pwd)
FILE=$(pwd)/files/$1
mkdir temp
cd temp && ino init
mv $FILE src/sketch.ino
cp $ROOT/bin/ino.ini $ROOT/temp/ino.ini
#ino build

#Clean up
cd $ROOT
rm -r -f temp/

