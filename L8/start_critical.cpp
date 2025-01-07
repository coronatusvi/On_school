#include <omp.h>
#include <stdio.h>

int f(int i){
    return i    ;
}

int main () {
    int temp[10], x[10], i;
    for(i = 0; i < 10; i++){
        x[i] = f(i);
    }
    #pragma omp parallel 
        #pragma omp for
        for(i = 0; i < 10; i++){
            #pragma omp atomic read
            temp[i] = x[f(i)];
            #pragma omp atomic write
            x[i] = temp[i]*2;
            #pragma omp atomic update
            x[i] *= 2;
            printf("x[%d] = %d\n", i, x[i]);
        }
    return 0;
}       