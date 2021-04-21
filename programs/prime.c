#include <stdio.h>
#include<stdlib.h>
#include <math.h>
#include <omp.h>

int eratosthenes(int lastNumber,int numOfThreads)
{
  const int lastNumberSqrt = (int)sqrt((double)lastNumber);

  int memorySize = (lastNumber-1)/2;

  char* isPrime = (char*)calloc(memorySize+1, sizeof(char));

  omp_set_num_threads(numOfThreads);

  #pragma omp parallel for
  {
    for (int i = 0; i <= memorySize; i++)
    {
      double start = omp_get_wtime();
      int my_thread_num = omp_get_thread_num();
      isPrime[i] = 1;
      double end = omp_get_wtime();
      fprintf(stderr,"%d:parallelfor_init:%lf\n",my_thread_num,(end-start));
    }
  }

  #pragma omp parallel for schedule(dynamic)
  {
    for (int i = 3; i <= lastNumberSqrt; i += 2){
      double start = omp_get_wtime();
      int my_thread_num = omp_get_thread_num();
      if (isPrime[i/2])
        for (int j = i*i; j <= lastNumber; j += 2*i)
          isPrime[j/2] = 0;
      double end = omp_get_wtime();
      fprintf(stderr,"%d:parallelfor_findodd:%lf\n",my_thread_num,(end-start));
    }
  }

  int numOfPrimes = lastNumber >= 2 ? 1 : 0;
  #pragma omp parallel for reduction(+:numOfPrimes)
  {
    for (int i = 1; i <= memorySize; i++){
      double start = omp_get_wtime();
      int my_thread_num = omp_get_thread_num();
      numOfPrimes += isPrime[i];
      double end = omp_get_wtime();
      fprintf(stderr,"%d:parallelfor_countprime:%lf\n",my_thread_num,(end-start));
    }
  }
  return numOfPrimes;
}

int main(int argc, char* argv[])
{
  
  if(argc != 3){
    printf("Wrong inputs provided... exiting");
    return 1;
  }

  int lastNumber = atoi(argv[1]);
  int numOfThreads = atoi(argv[2]);
  int numOfPrimes = eratosthenes(lastNumber,numOfThreads);
  
  printf("Total Number of Primes between 2 and %d: %d\n",lastNumber,numOfPrimes);
  return 0;
}
