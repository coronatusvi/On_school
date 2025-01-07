#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel
    {
        printf("Hello World\n");
    }
    return 0;
}

//OMP_NUM_THREADS=20