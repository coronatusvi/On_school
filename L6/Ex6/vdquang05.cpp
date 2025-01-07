#include <iostream>
#include <cmath>
#include <iomanip>
#include <omp.h>
#include <vector>

using namespace std;

int main() {
    int n = 10;
    double h = 1.0 / n;
    vector<double> partial_pis(n, 0.0);
    double start_time, end_time;

    start_time = omp_get_wtime();

    #pragma omp parallel 
    {
        int thread_id = omp_get_thread_num();
        #pragma omp for
        for (int i = 0; i < n; ++i) {
            double x = (i + 0.5) * h;
            partial_pis[i] = sqrt(1.0 - x * x);
            cout << "Thread " << thread_id << ", partial pi [" << i << "]: " << fixed << setprecision(10) << partial_pis[i] << endl;
        }
    }
    
    double pi = 0.0;
    for(double partial_pi : partial_pis) {
        pi += partial_pi;
    }
    
    pi *= 4.0 * h;
  
    end_time = omp_get_wtime();
    double seconds = end_time - start_time;

    cout << "\nEstimated Pi (Check Reduction): " << fixed << setprecision(10) << pi << endl;
    cout << "Time: " << fixed << setprecision(3) << seconds << "s" << endl;
    return 0;
}                   