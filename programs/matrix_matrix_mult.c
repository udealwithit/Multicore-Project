#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

/*
 * Example program to multiply matrix and matrix
 * Uses openmp to parallelize the application
*/

int rows = 0;
int columns = 0;
int columns2 = 0;

double mat_mul_row_col(int size, int row, int col, double **mat1, double **mat2) {
    /*
     * Function to multiply one row of matrix with one column of another matrix
     * This will be used in matrix multiplication where each thread
    */
    double result = 0.0;
    for(int i=0; i<size; i++) {
        result += mat1[row][i] * mat2[i][col];
    }
    return result;
}

int main(int argc, char* argv[]) 
{
    /*
     * Program takes as input rows, columns, columns2, num_threads, matrix_file and 2nd matrix_file
    */
    if (argc != 7) {
        printf("Wrong inputs provided... exiting");
        return 1;
    }

    rows = atoi(argv[1]);
    columns = atoi(argv[2]);
    columns2 = atoi(argv[3]);
    int num_threads = atoi(argv[4]);
    FILE* mat_file = fopen(argv[5], "r");
    FILE* mat_file2 = fopen(argv[6], "r");

    if (mat_file==NULL || mat_file2==NULL) {
        printf("Error opening given file... exiting");
        return 1;
    }

    double **matrix1 = calloc(rows, sizeof(double*));//[rows][columns];
    double **matrix2 = calloc(columns, sizeof(double*));//[columns][columns2];
    double **result_mat = calloc(rows, sizeof(double*));//[rows][columns2];

    for(int i=0; i<rows; i++) {
        matrix1[i] = calloc(columns, sizeof(double));
    }
    for(int i=0; i<columns; i++) {
        matrix2[i] = calloc(columns2, sizeof(double));
    }
    for(int i=0; i<rows; i++) {
        result_mat[i] = calloc(columns2, sizeof(double));
    }

    int total_multiplications = rows * columns2;

    for(int i=0; i<rows; i++) {
        for(int j=0; j<columns; j++) {
            fscanf(mat_file, "%lf", &matrix1[i][j]);
        }
    }

    for(int i=0; i<columns; i++) {
        for(int j=0; j<columns2; j++) {
            fscanf(mat_file2, "%lf", &matrix2[i][j]);
        }
    }

    fclose(mat_file);
    fclose(mat_file2);

    #pragma omp parallel for num_threads(num_threads)
    for(int i=0; i<total_multiplications; i++) {
        int my_rank = omp_get_thread_num();
        double start = omp_get_wtime();
        
        int r = i/columns2;
        int c = i%columns2;
        result_mat[r][c] = mat_mul_row_col(columns, r, c, matrix1, matrix2);

        double end = omp_get_wtime();
        fprintf(stderr, "%d:parallelfor:%lf\n", my_rank, end - start);
    }

    printf("Result Matrix: \n");
    for(int i=0; i<rows; i++) {
        for(int j=0; j<columns2; j++) {
            printf("%lf ", result_mat[i][j]);
        }
        printf("\n");
    }
}