#include <iostream>
#include <omp.h>

const int N = 500; 
double A[N][N], x[N], y[N];

void initialize() {

    for (int i = 0; i < N; ++i) {
        x[i] = i * 1.0;
        for (int j = 0; j < N; ++j) {
            A[i][j] = i + j * 1.0;
        }
    }
}

void matrixVectorMultiplication() {

    for (int i = 0; i < N; ++i) {
        y[i] = 0.0;
    }

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            y[i] += A[i][j] * x[j];
        }
    }
}

int main() {
    initialize();
    matrixVectorMultiplication();

    for (int i = 0; i < N; ++i) {
        std::cout << "y[" << i << "] = " << y[i] << std::endl;
    }

    return 0;
}