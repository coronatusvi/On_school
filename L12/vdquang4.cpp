#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel
    {
        int nthreads = omp_get_num_threads();
        int thread_num = omp_get_thread_num();
        printf("Threads entering parallel region:%d\n", nthreads);

        #pragma omp for
        for (int iter = 0; iter < nthreads; iter++)
            printf("thread %d executing iter %d\n", thread_num, iter);
    }
    return 0;
}

// First:
// Threads entering parallel region:2
// thread 0 executing iter 0
// Threads entering parallel region:2
// thread 1 executing iter 1

// Second: OMP_NUM_THREADS=8
// Threads entering parallel region:8
// thread 2 executing iter 2
// Threads entering parallel region:8
// thread 1 executing iter 1
// Threads entering parallel region:8
// thread 4 executing iter 4
// Threads entering parallel region:8
// thread 6 executing iter 6
// Threads entering parallel region:8
// thread 7 executing iter 7
// Threads entering parallel region:8
// thread 3 executing iter 3
// Threads entering parallel region:8
// Threads entering parallel region:8
// thread 5 executing iter 5
// thread 0 executing iter 0
