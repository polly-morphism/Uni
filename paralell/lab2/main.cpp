#include "omp.h"
#include <stdio.h>
#include <iostream>
#include <unordered_map>
#define N 400


int main() {
    std::unordered_map<unsigned,std::string> map{
    {200505,"2.5"},{200805,"3.0"},{201107,"3.1"},{201307,"4.0"},{201511,"4.5"},{201811,"5.0"},{202011,"5.1"}};
    std::cout << "OpenMP found" << map.at(_OPENMP) << ".\n";
	double start, end, tick;

	start = omp_get_wtime();
	std::cout << "Non-parallel\n\n";
	end = omp_get_wtime();
    tick = omp_get_wtick();
	std::cout << "Without parallelism: " << end - start << "\n\n";
    std::cout << "Accuracy of timer: " << tick << "\n\n";

	start = omp_get_wtime();
  #pragma omp parallel
  {
      printf("Hello World... from thread = %d\n",
             omp_get_thread_num());
  }

	end = omp_get_wtime();
	std::cout << "\nResult with threads: " << end - start;

	std::cout << "\n\nMatrix task:" << std::endl;
	double a[N][N], b[N][N], c[N][N];
	int i, j, k, sum, sum_2;
	for (i = 0; i < N; i++) {
		for (j = 0; j < N; j++) {
			a[i][j] = b[i][j] = rand() % 10;
		}
	}

	start = omp_get_wtime();
	for (i = 0; i < N; i++) {
		for (j = 0; j < N; j++) {
			c[i][j] = 0.0;
			for (k = 0; k < N; k++) c[i][j] += a[i][k] * b[k][j];
		}
	}
	end = omp_get_wtime();
	std::cout << "\nResult without threads: " << end - start << "\n";

	start = omp_get_wtime();
	#pragma omp parallel for private(i, j, k)
	for (i = 0; i < N; i++) {
		for (j = 0; j < N; j++) {
			c[i][j] = 0.0;
			for (k = 0; k < N; k++) c[i][j] += a[i][k] * b[k][j];
		}
	}
	end = omp_get_wtime();
	std::cout << "Result with parallel: " << end - start << "\n\n";


    start = omp_get_wtime();
    #pragma omp
    #pragma omp parallel shared(a) private(i,j,sum)
    #pragma omp for
    for(i=0; i <N; i++) {
        sum =0;
        for(j=0; j <N; j++)
            sum +=a[i][j];
            printf ("Summary of elems in row %d equals %d\n",i,sum);
            } /* Завершение параллельного фрагмента */
    end = omp_get_wtime();
    printf("Execution time: %f", end - start);
    printf("\n\n");
    start = omp_get_wtime();
    int total = 0;
    #pragma omp
    #pragma omp parallel for shared(a) private(i,j,sum_2) reduction (+:total)
        for(i=0; i < N; i++) {
            sum_2 = 0;
            for(j=0; j < N; j++){
                sum_2 +=a[i][j];
            }
            printf ("Summary of elems in row %d equals %d\n",i,sum_2);
    total = total +sum_2;
        }
    printf("Total summary:%d\n", total);
    end = omp_get_wtime();
    printf("Execution time: %f\n", end - start);

	return 0;
}
