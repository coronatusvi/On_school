#include <iostream>
#include <omp.h>

long long fibonacci(int n) {
    if (n <= 1) return 1;

    long long f1, f2;

    #pragma omp task shared(f1)
    f1 = fibonacci(n - 1);

    #pragma omp task shared(f2)
    f2 = fibonacci(n - 2);

    #pragma omp taskwait
    return f1 + f2;
}

int main() {
    int n;
    std::cout << "Nhập n cho dãy Fibonacci: ";
    std::cin >> n;

    long long result;
    #pragma omp parallel
    {
        #pragma omp single
        result = fibonacci(n);
    }

    std::cout << "F(" << n << ") = " << result << std::endl;
    return 0;
}
