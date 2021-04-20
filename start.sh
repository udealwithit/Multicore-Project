#!/bin/bash

rm -rf build
mkdir build
gcc -fopenmp -Wall -o "build/temp" "programs/$1"
./build/temp "${@:2}" 2> build/prof

python3 visualization/main.py
echo "Done profiling the program. You can have a look at the visualizations"