#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/*
 * Example program to count the number of times a number occures in a list
 * Uses openmp to parallelize the application
*/

int main(int argc, char* argv[])
{
    /*
     * Program takes as input file, size, the number to search and num_threads
    */
    if (argc != 5) {
        printf("Wrong inputs provided... exiting");
        return 1;
    }

    FILE* input_file = fopen(argv[1], "r");
    int size = atoi(argv[2]);
    int number = atoi(argv[3]);
    int num_threads = atoi(argv[4]);
    int count = 0;

    if (input_file == NULL) {
        printf("Error opening given file... exiting");
        return 1;
    }

    int list_nums[size];

    for(int i=0; i<size; i++) {
        fscanf(input_file, "%d ", &list_nums[i]);
    }

    #pragma omp parallel for num_threads(num_threads)
    for(int i=0; i<size; i++) {
        int my_rank = omp_get_thread_num();
        double start = omp_get_wtime();
        if(list_nums[i] == number) {

            double start_atm = omp_get_wtime();
            #pragma omp atomic
            count += 1;
            double end_atm = omp_get_wtime();
            
            fprintf(stderr, "%d:atomic:%lf\n", my_rank, (end_atm - start_atm));
        }
        double end = omp_get_wtime();
        fprintf(stderr, "%d:parallelfor:%lf\n", my_rank, (end - start));
    }

    printf("Number of times %d occured is %d\n", number, count);
}