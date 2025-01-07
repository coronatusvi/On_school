#include <stdio.h>
#include <omp.h>

int main() {
    int sum = 0;

    #pragma omp parallel
    {
        #pragma omp atomic
        sum += 1; 
    }

    printf("Tong la: %d\n", sum);
    return 0;
}
