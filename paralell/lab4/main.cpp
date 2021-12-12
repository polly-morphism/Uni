#include <iostream>
#include <cstdlib>
#include <ctime>
#include "omp.h"
using namespace std;

double**
matrixCreation(int n)
{
  double** matrix = new double*[n];
  for (int i = 0; i < n + 1; i++) {
    matrix[i] = new double[n + 1];
  }
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n + 1; j++) {
      matrix[i][j] = rand() % 100 + 1;
    }
  }
  return matrix;
}
void
matrixPrinting(double** matrix, int n)
{
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n + 1; j++) {
      if (j < n && j != 0) {
        printf("+\t%.1fx%d\t", matrix[i][j], j + 1);
      } else if (j < n) {
        printf("%.1fx%d\t", matrix[i][j], j + 1);
      } else {
        printf("=%.1f\t", matrix[i][j]);
      }
    }
    printf("\n");
  }
}

double*
gauseSolving(double** m, int n, bool parallel)
{

  double** matrix = new double*[n];
  for (int i = 0; i < n + 1; i++) {
    matrix[i] = new double[n + 1];
  }

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n + 1; j++) {
      matrix[i][j] = m[i][j];
    }
  }

  double* res = new double[n];
  int i, j, k;
  double temp;
  for (i = 0; i < n; i++) {
    temp = matrix[i][i];
    for (k = 0; k < n + 1; k++) {
      matrix[i][k] /= temp;
    }
#pragma omp parallel for shared(matrix, i, n), private(j, k, temp) default(    \
                                                 none) if (parallel)
    for (j = i + 1; j < n; j++) {
      temp = matrix[j][i];
      for (k = 0; k < n + 1; k++) {
        matrix[j][k] -= matrix[i][k] * temp;
      }
    }
  }

  res[n - 1] = matrix[n - 1][n];

  for (i = n - 2; i >= 0; i--) {
    res[i] = matrix[i][n];
#pragma omp parallel for shared(res, matrix, i,                                \
                                n) private(j) default(none) if (parallel)
    for (j = i + 1; j < n; j++) {
      res[i] -= matrix[i][j] * res[j];
    }
  }
  return res;
}

void
resPrinting(double* res, int n)
{
  for (int i = 0; i < n; i++) {
    cout << "x_" << i + 1 << ": " << res[i] << endl;
  }
}

int
main()
{
  int user_number_of_threads, dimensions;
  std::cout << "\nThreads: n=";
  std::cin >> user_number_of_threads;
  std::cout << "Dimensions: n=";
  std::cin >> dimensions;
  srand((unsigned)time(NULL));

  double** matrix = matrixCreation(dimensions);
  double time1, time2;
  time1 = omp_get_wtime();
  double* res = gauseSolving(matrix, dimensions, false);
  time2 = omp_get_wtime();
  if (dimensions < 15) {
    cout << "Printing the generated " << dimensions << "-dimensional matrix."
         << endl;
    matrixPrinting(matrix, dimensions);
  }

  cout << "Algorithm wihtout omp: " << time2 - time1 << " sec." << endl;

  omp_set_num_threads(user_number_of_threads);
  time1 = omp_get_wtime();
  res = gauseSolving(matrix, dimensions, true);
  time2 = omp_get_wtime();
  cout << "Algorithm with omp " << user_number_of_threads
       << " threads: " << time2 - time1 << " sec." << endl;
  if (dimensions < 30) {
    resPrinting(res, dimensions);
  }
  cout << endl;
  return 0;
}
