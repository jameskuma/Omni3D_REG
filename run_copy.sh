#!/usr/bin/env bash

echo $1 $2 &&
mkdir -p "OO3D/$1" && 
cp -r "$2/standard/images" "OO3D/$1/" && 
cp -r "$2/standard/matting" "OO3D/$1/" && 
cp -r "$3/Scan/Scan.obj" "OO3D/$1/"