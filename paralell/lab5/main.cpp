#include <ctime>
#include "omp.h"
#include <iostream>
#include "random"
#define SEED 123456
#define N 1000000000000
#include <climits>

unsigned int seed = 676767676;



double randUint( long i ){

	seed = seed * 1103515245 + 123456;

    return seed / (double)UINT_MAX ;
}

double f(double y) { return (4.0 / (1.0 + y * y)); }

int main() {
    std::cout << "First task:" << std::endl;

   double w, x, sum, pi, time1, time2;
   int i;
   w = 1.0 / N;
   sum = 0.0;

   time1 = omp_get_wtime();
   for (i = 0; i < N; i++) {
       x = w * (i - 0.5);
       sum = sum + f(x);
   }
   time2 = omp_get_wtime();
   std::cout << "Time with in sync: " << time2 - time1 << std::endl;
   pi = w * sum;
   printf("pi = %f\n", pi);

   sum = 0;

   time1 = omp_get_wtime();
#pragma omp parallel for private(x) shared(w) reduction(+:sum)
   for (i = 0; i < N; i++) {
       x = w * (i - 0.5);
       sum = sum + f(x);
   }
   time2 = omp_get_wtime();
   std::cout << "Time in parallel: " << time2 - time1 << std::endl;
   pi = w * sum;
   printf("pi = %f\n", pi);

    std::cout << "Second task (Monte-Carlo method):" << std::endl;

    long count=0;
    pi = 0;

    #pragma omp parallel for reduction(+: count)
    for (long i=0; i<N; i++) {


        double x,y;
        x = randUint(i);
        y = randUint(i);


        if (x*x+y*y <= 1)
            count = count + 1;


    }

    pi=((double)count/(double)N) * 4.0;

    printf("Result with openmp : pi is %1.16f \n",pi);

    return 0;

}
