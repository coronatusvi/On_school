#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

int main() {
    long long num_points = 1000000;
    long long points_inside = 0;
    double pi_estimate;

    #pragma omp parallel reduction(+:points_inside)
    {
        unsigned int seed = time(NULL) ^ omp_get_thread_num(); 
        for (long long i = 0; i < num_points / omp_get_num_threads(); i++) {
            double x = (double)rand_r(&seed) / RAND_MAX; // Random x
            double y = (double)rand_r(&seed) / RAND_MAX; // Random y

            if (x*x + y*y <= 1.0) {
                points_inside++;
            }
        }
    }
    printf("%lld", points_inside);
    pi_estimate = 4.0 * points_inside / num_points;
    printf("Ước lượng Pi = %f\n", pi_estimate);

    return 0;
}