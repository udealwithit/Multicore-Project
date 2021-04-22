#!/bin/bash

rm -rf build
rm -rf output
mkdir build
mkdir output
clear
echo "Enter the program to profile and visualize"
echo "1. Matrix Vector Multiplication"
echo "2. Matrix Matrix Multiplication"
echo "3. Producer Consumer Problem"
echo "4. Search an element in array"
echo "5. Find all prime numbers till a given number"
read program

declare -a arguments=()
declare -a x=()

clear
case $program in
    1)
        echo "Matrix Vector Multiplication"
        gcc -fopenmp -Wall -o "build/temp" "programs/matrix_vect_mult.c"
        echo "Enter number of rows of Matrix"
        read rows
        arguments+=("$rows")
        echo "Enter number of columns of Matrix (rows of vector)"
        read cols
        arguments+=("$cols")
        echo "Enter number of threads to run"
        read threads
        arguments+=("$threads")
        python3 helpers/number_generator.py 1 $rows $cols 500 "build/mat1"
        python3 helpers/number_generator.py 0 $rows $cols 500 "build/vec1"
        arguments+=("mat1")
        arguments+=("vec1")
        ;;
    2)
        echo "Matrix Matrix Multiplication"
        gcc -fopenmp -Wall -o "build/temp" "programs/matrix_matrix_mult.c"
        echo "Enter number of rows of 1st Matrix"
        read rows
        arguments+=("$rows")
        echo "Enter number of columns of 1st Matrix"
        read cols1
        arguments+=("$cols1")
        echo "Enter number of columns of 2nd Matrix"
        read cols2
        arguments+=("$cols2")
        echo "Enter number of threads to run"
        read threads
        arguments+=("$threads")
        python3 helpers/number_generator.py 1 $rows $cols1 500 "build/mat1"
        python3 helpers/number_generator.py 1 $cols1 $cols2 500 "build/mat2"
        arguments+=("mat1")
        arguments+=("mat2")
        ;;
    3)
        gcc -fopenmp -Wall -o "build/temp" "programs/ProducerConsumer.c"
        echo "Enter the size of the queue"
        read size
        arguments+=("$size")
        echo "Enter the number of consumer threads"
        read consumer_threads
        arguments+=("$consumer_threads")
        echo "Enter the total number of elements to be produced"
        read numberofele
        arguments+=("$numberofele")
        ;;
    4)
        gcc -fopenmp -Wall -o "build/temp" "programs/occurence_count.c"
        echo "Enter size of array"
        read size
        arguments+=("$size")
        echo "Enter the number to search"
        read num
        arguments+=("$num")
        echo "Enter number of threads to run"
        read threads
        arguments+=("$threads")
        python3 helpers/number_generator.py 2 $size 0 500 "build/arr"
        arguments+=("arr")
        ;;
    5)
        gcc -fopenmp -Wall -o "build/temp" "programs/prime.c"
        echo "Enter till which number to find the primes"
        read lastNumber
        arguments+=("$lastNumber")

        echo "Enter number of threads to run"
        read threads
        arguments+=("$threads")
        ;;
esac

cd build

clear
echo "1. Run Massif tool (This takes time)"
echo "2. Run Cachegrind tool"
echo "3. Run both the tools (May take sometime)"
read choice

./temp "${arguments[@]}" > prog_out 2> prof

if [ $choice == 1 ]
then
    valgrind --tool=massif --stacks=yes --time-unit=ms --log-file="valgrind_log" ./temp "${arguments[@]}" > /dev/null 2> /dev/null
    ms_print massif.out.* > massif_log
elif [ $choice == 2 ]
then
    valgrind --tool=callgrind --simulate-cache=yes --separate-threads=yes --log-file="valgrind_log" ./temp "${arguments[@]}" > /dev/null 2> /dev/null
    for c in `ls callgrind.out.*-*`
    do
        callgrind_annotate --auto=yes "$c" > "callgrind_log-$c"
    done
    x=`ls callgrind_log-*`
else
    valgrind --tool=massif --stacks=yes --time-unit=ms --log-file="valgrind_log" ./temp "${arguments[@]}" > /dev/null 2> /dev/null
    ms_print massif.out.* > massif_log
    valgrind --tool=callgrind --simulate-cache=yes --separate-threads=yes --log-file="valgrind_log" ./temp "${arguments[@]}" > /dev/null 2> /dev/null
    for c in `ls callgrind.out.*-*`
    do
        callgrind_annotate --auto=yes "$c" > "callgrind_log-$c"
    done
    x=`ls callgrind_log-*`
fi


cd ..
python3 visualization/main.py ${x[@]}
echo "Done profiling the program. The program output is in build/prog_out"
echo "You can have a look at the profiling information in the output folder"