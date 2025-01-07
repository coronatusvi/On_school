#include <stdio.h>
#include <omp.h>

float f(float x) { return 1; }
float g(float x) { return 2; }
float h(float x) { return 3; }

int main() {
    float fx, gx, hx, s;

    #pragma omp parallel sections
    {
        #pragma omp section
        fx = f(1.0);

        #pragma omp section
        gx = g(1.0);

        #pragma omp section
        hx = h(1.0);
    }

    s = fx + gx + hx;
    printf("Tổng s = %f\n", s);

    return 0;
}