#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <omp.h>
#include <string.h>

/*
 * Example program to implement producer consumer problem.
 * Uses openmp to parallelize the application
*/
int front = -1, rear = -1;

int isEmpty(){
    if(front == -1){
        return 1;
    }
    return 0;
}

int isFull(int size){
    if(rear == size-1){
        return 1;
    }
    return 0;
}

void generateRandomFile(int elem,int thread_num,int request_per_thread){
    // printf("GenerateRadnom");
    char filename[20];
    snprintf(filename,20,"RandNum_%d_%d",thread_num,request_per_thread);
    FILE* rand_file = fopen(filename, "w");
    for(int i = 0;i<elem;i++){
        fprintf(rand_file,"%d ",rand());
    }
    fclose(rand_file);
}

int enQueue(int value,int *items, int size) {
    // printf("ENQUEUE\n");
    // for(int i=0;i<size;i++){
    //     printf("%d ",items[i]);
    // }
    // printf("\n");
    if (rear == size - 1){
        return -1;
    }
    else {
        if (front == -1)
            front = 0;
        rear+=1;
        items[rear] = value;
        return 0;
    }
}

int deQueue(int *items) {
    // printf("DEQUEUE\n");
    // for(int i=0;i<3;i++){
    //     printf("%d ",items[i]);
    // }
    // printf("\n");
    if (front == -1)
    {
        return -1;
    }
    else {
        int elem = items[front];
        front+=1;
        if (front > rear){
            front = rear = -1;
        }
        return elem;
    }
}

void producer(int *items,int count, int total_elem,int size){
    // printf("PRCOUNT %d %d",count,total_elem);
    while(count<total_elem){
        int val = 50 + rand() %1000;
        int elem = -1;
        double start = omp_get_wtime();
        #pragma omp critical
        {
            double end = omp_get_wtime();
            fprintf(stderr,"0:critical wait:%lf\n",(end-start));
            if(isFull(size) != 1){
                elem = enQueue(val,items,size);
            }
            end = omp_get_wtime();
            fprintf(stderr,"0:critical:%lf\n",(end-start));
        }
        if(elem != -1){
            count+= 1;
        }
        sleep(1);
    }
}

void consumer(int *items,int count,int total_elem,int thread_num,int *request_per_thread){
    while(count<total_elem){
        int elem = -1;
        double start = omp_get_wtime();
        #pragma omp critical
        {
            double end = omp_get_wtime();
            fprintf(stderr,"%d:critical wait:%lf\n",thread_num,(end-start));
            if(isEmpty() != 1){
                elem = deQueue(items);
            }
            end = omp_get_wtime();
            fprintf(stderr,"%d:critical:%lf\n",thread_num,(end-start));
        }
        if(elem != -1){
            *request_per_thread += 1;
            start = omp_get_wtime();
            generateRandomFile(elem,thread_num,*request_per_thread);
            double end = omp_get_wtime();
            fprintf(stderr,"%d:generateRandomFile:%lf\n",thread_num,(end-start));
        }
        else{
            sleep(2);
        }
        count += 1;
    }
}

int main(int argc, char* argv[]) 
{
    /*
     * Program takes as input rows, columns, num_threads, matrix_file and vector_file
    */
    if (argc != 5) {
        printf("Wrong inputs provided... exiting");
        return 1;
    }



    int *items = calloc(atoi(argv[1]),sizeof(int));
    int size = atoi(argv[1]);
    int consumer_threads = atoi(argv[2]);
    int producer_threads = atoi(argv[3]);
    int total_threads = consumer_threads+producer_threads;
    int total_elements = atoi(argv[4]);
    int count,request_per_thread;
    #pragma omp parallel shared(items,front,rear,size,total_elements) private(count,request_per_thread) num_threads(total_threads)
    {
        count = 0;
        request_per_thread = 0;
        int my_thread_num = omp_get_thread_num();
        // printf("ThreadNUm %d\n",my_thread_num);

        double start = omp_get_wtime();
        if(my_thread_num != 0){
            // printf("CONSUMER\n");
            consumer(items,count,total_elements,my_thread_num,&request_per_thread);
        }
        else{
            // printf("PRODUCER\n");
            producer(items,count,total_elements,size);
        }
        double end = omp_get_wtime();
        fprintf(stderr,"%d:parallel:%lf\n",my_thread_num,(end-start));
    }

}

