# Multicore-Project
Visualization tool for parallel programs

## Running the project
Run `./start.sh` command to startup the tool
You can then choose the program which you would like to profile and visualize
It then asks for the input for the chosen program
The tool has a helper code to generate matrix or vector of given size with random numbers. It generates numbers from 0 to 500.

The programs and their inputs are
1. Matrix Vector Multiplication <br>
   Row and Column size of first matrix <br>
   Rows of the vector (same as columns of matrix) <br>
   Number of threads to use <br>
   
2. Matrix Matrix Multiplication <br>
   Row and Column size of first matrix <br>
   Rows(same as columns of 1st matrix) and Column size of second matrix <br>
   Number of threads to use <br>
   
3. Producer Consumer <br>
   Size of the queue <br>
   Number of consumer threads (total threads will be 1 + consumer threads as 1 will be a producer thread) <br>
   Total elements to consume <br>

4. Finding the occurence of a number in an array <br>
   Size of array in which to search (the array will be generated randomly) <br>
   The number to search <br>
   The number of threads to use <br>

5. Finding the number of primes till a given range. <br>
   The number till which to find primes <br>
   The number of threads to use <br>
   
After this the script will ask for the valgrind tool to use for profiling (Massif, Callgrind or both) and the output visualizations will be in the output folder created. The program output will be in build/prog_out file.
