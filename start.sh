#!/bin/bash

rm -rf build
rm -rf output
mkdir build
mkdir output
gcc -fopenmp -Wall -o "build/temp" "programs/$1"
cd build

echo "1. Run Massif tool (This takes time)"
echo "2. Run Cachegrind tool"
read choice

./temp "${@:2}" 2> prof

if [ $choice == 1 ]
then
    valgrind --tool=massif --stacks=yes --time-unit=ms --log-file="valgrind_log" ./temp "${@:2}" > /dev/null 2> /dev/null
    ms_print massif.out.* > massif_log
else
    valgrind --tool=callgrind --simulate-cache=yes --log-file="valgrind_log" ./temp "${@:2}" > /dev/null 2> /dev/null
    callgrind_annotate --auto=yes callgrind.out.* >callgrind_log
fi

cd ..
python3 visualization/main.py
echo "Done profiling the program. You can have a look at the visualizations"