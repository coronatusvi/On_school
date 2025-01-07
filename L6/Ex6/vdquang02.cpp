#include <iostream>
#include <cmath>
#include <iomanip>
#include <omp.h>

using namespace std;

int main() {
  int n = 10000000;
  double h = 1.0 / n;
  double pi = 0.0;
  double start_time, end_time;

  start_time = omp_get_wtime();

  #pragma omp parallel
  {
      double local_pi = 0.0;
      #pragma omp for
      for (int i = 0; i < n; ++i) {
          double x = (i + 0.5) * h;
          local_pi += sqrt(1.0 - x * x);
      }
      #pragma omp critical
      pi += local_pi;
  }
    
  pi *= 4.0 * h;

  end_time = omp_get_wtime();

  double seconds = end_time - start_time;


  cout << "Estimated Pi (Parallel with #pragma omp parallel): " << fixed << setprecision(10) << pi << endl;
  cout << "Time: " << fixed << setprecision(3) << seconds << "s" << endl;
  return 0;
}