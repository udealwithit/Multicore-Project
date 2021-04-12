#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/*
 * Example program to multiply matrix and vector
 * Uses openmp to parallelize the application
*/

double vector_mult(int size, double* vect1, double* vect2) {
    /*
     * Function to multiply one column vector with another
     * This will be used in matrix multiplication where each thread
     * multiplies one row of the matrix with the vector
    */
    double result = 0.0;
    for(int i=0; i<size; i++) {
        result += vect1[i]*vect2[i];
    }
    return result;
}

int main(int argc, char* argv[]) 
{
    /*
     * Program takes as input rows, columns, num_threads, matrix_file and vector_file
    */
    if (argc != 6) {
        printf("Wrong inputs provided... exiting");
        return 1;
    }

    int rows = atoi(argv[1]);
    int columns = atoi(argv[2]);
    int num_threads = atoi(argv[3]);
    FILE* mat_file = fopen(argv[4], "r");
    FILE* vect_file = fopen(argv[5], "r");

    if (mat_file==NULL || vect_file==NULL) {
        printf("Error opening given file... exiting");
        return 1;
    }

    double matrix[rows][columns];
    double vector[columns];
    double result_vect[rows];

    for(int i=0; i<rows; i++) {
        for(int j=0; j<columns; j++) {
            fscanf(mat_file, "%lf", &matrix[i][j]);
        }
    }

    for(int i=0; i<columns; i++) {
        fscanf(vect_file, "%lf", &vector[i]);
    }

    // Calculate the work for each thread
    // For e.g if we have 5 rows and 5 threads each thread will
    // multiply 1 row of matrix with vector
    int size_of_work = (rows + 1)/num_threads;

    #pragma omp parallel num_threads(num_threads)
    {
        int my_rank = omp_get_thread_num();
        int my_start = my_rank * size_of_work;
        int my_end = (my_rank == num_threads - 1) ? rows : my_start + size_of_work;

        for(int i=my_start; i<my_end; i++) {
            result_vect[i] = vector_mult(columns, matrix[i], vector);
        }
    }

    printf("Result vector is: \n");
    for(int i=0; i<rows; i++) {
        printf("%lf ", result_vect[i]);
    }
    printf("\n");

    return 0;
}