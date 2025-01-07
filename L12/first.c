#include<stdio.h>
#include<omp.h>

int main () {
    // double a[1000], b[1000], c[1000];
    
    // for (int i = 0; i < 1000; i++) {
    //     c[i] = a[i] + b[i];
    // }
    {
        int id = omp_get_thread_num();
        printf("Hello World from thread %d\n", id);
    }
    return 0;
}