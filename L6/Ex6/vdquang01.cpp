#include <iostream>
#include <cmath>
#include <iomanip>

#ifdef _OPENMP
#include <omp.h>
#endif
using namespace std;

int main() {
  int n = 10000000;
  double h = 1.0 / n;
  double pi = 0.0;
  double start_time, end_time;

  #ifdef _OPENMP
      start_time = omp_get_wtime();
  #else
       start_time = 0; // For sequential case we use 0 
  #endif

  for (int i = 0; i < n; ++i) {
    double x = (i + 0.5) * h;
    pi += sqrt(1.0 - x * x);
  }
  
  pi *= 4.0 * h;

  #ifdef _OPENMP
      end_time = omp_get_wtime();
  #else
      end_time = 0;
  #endif

  double seconds = end_time - start_time;

  cout << "Estimated Pi (Sequential): " << fixed << setprecision(10) << pi << endl;
  cout << "Time: " << fixed << setprecision(3) << seconds << "s" << endl;

  return 0;
}