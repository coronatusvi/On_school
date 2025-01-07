#include<iostream>
#include<omp.h>

using namespace std;

float f (float x) {return x;}
float g (float x) {return x;}
float h (float x) {return x;}

int main () {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    float sum = 0;
    double start_time = omp_get_wtime(); // Bắt đầu đo thời gian

    #pragma omp parallel sections reduction(+:sum)
    {
        #pragma omp section
            sum += f(1.);
        #pragma omp section
            sum += g(2.);
        #pragma omp section
            sum += h(3.);
    }
    cout << "Reduction clause: " << sum << endl;
    cout << "Time: " << omp_get_wtime() - start_time << endl;
return 0;}  