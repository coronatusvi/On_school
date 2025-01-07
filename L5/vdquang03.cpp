#include <iostream>
#include <cmath>
#include <omp.h>

bool isPrimeParallel(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    bool is_prime = true;
    int limit = static_cast<int>(std::sqrt(n));

    #pragma omp parallel for schedule(guided) shared(is_prime)
    for (int i = 5; i <= limit; i += 6) {
        if (!is_prime) continue; 
        if (n % i == 0 || n % (i + 2) == 0) {
            #pragma omp atomic write
            is_prime = false;
        }
    }
    return is_prime;
}

int main() {
    int number;
    std::cin >> number;

    bool resultParallel = isPrimeParallel(number);
    std::cout << number << (resultParallel ? " là số nguyên tố" : " không phải số nguyên tố") << std::endl;

    return 0;
}