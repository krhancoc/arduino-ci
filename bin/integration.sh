#!/bin/bash
ROOT=$(pwd)
FILE=$(pwd)/files/$1
mkdir temp
echo $FILE moved to temporary project... calling ino init...
cd temp && ino init
mv $FILE src/sketch.ino
cp $ROOT/bin/ino.ini $ROOT/temp/ino.ini
echo Copying done... calling ino build
ino build
ino upload
echo Cleaning up...
#Clean up
cd $ROOT
rm -r -f temp/

