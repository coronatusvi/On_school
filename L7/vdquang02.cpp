#include <stdio.h>
#include <omp.h>

float f(float x) { return 1; }
float g(float x) { return 2; }
float h(float x) { return 3; }

int main() {
    float fx, gx, hx, s = 0; 

    #pragma omp parallel sections reduction(+:s)
    {
         #pragma omp section
        {
            fx = f(1.0);
             s += fx;
        }

        #pragma omp section
         {
            gx = g(1.0);
            s+=gx;
        }

        #pragma omp section
        {
            hx = h(1.0);
            s+=hx;
        }
    }

    printf("Tổng s = %f\n", s);

    return 0;
}