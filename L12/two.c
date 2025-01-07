#include<stdio.h>

int main () {
    int tn, tm, tp;
    tn=omp_get_num_threads();
    tm=omp_get_max_threads();
    tp=omp_get_num_procs();

    printf("Sequental:%2d cores:%2d max:%2d\n", tn, tm, tp);

    {
    tn:omp_get_thread_num();
    }
    return 0;
}