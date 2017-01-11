#!/bin/bash

cd ..
FILE=files/$1

mkdir temp && cd temp
ino init
mv $FILE src/
ino build

