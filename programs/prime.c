#include <stdio.h>
#include<stdlib.h>
#include <math.h>
#include <omp.h>
const int lastNumber = 1000;

int eratosthenes(int lastNumber)
{
  const int lastNumberSqrt = (int)sqrt((double)lastNumber);

  int memorySize = (lastNumber-1)/2;

  // initialize
  char* isPrime = (char*)calloc(memorySize+1, sizeof(char));
#pragma omp parallel for
  for (int i = 0; i <= memorySize; i++)
    isPrime[i] = 1;

  // find all odd non-primes
#pragma omp parallel for schedule(dynamic)
  for (int i = 3; i <= lastNumberSqrt; i += 2)
    if (isPrime[i/2])
      for (int j = i*i; j <= lastNumber; j += 2*i)
        isPrime[j/2] = 0;

  // sieve is complete, count primes
  int found = lastNumber >= 2 ? 1 : 0;
#pragma omp parallel for reduction(+:found)
  for (int i = 1; i <= memorySize; i++)
    found += isPrime[i];
   return found;
}

int main(int argc, char* argv[])
{
  /* gcc -fopenmp -Wall -std=c99 -o prime prime.c -lm */
  printf("Primes between 2 and %d\n\n", lastNumber);
  printf("Only odd numbers, OpenMP\n");
  int found = eratosthenes(lastNumber);
  printf("%d primes found.\n\n", found);
  return 0;
}
