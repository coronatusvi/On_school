#include <iostream>
#include <omp.h>

int main() {
    // Get the maximum number of threads
    int max_threads = omp_get_max_threads();

    // Print the maximum number of threads
    std::cout << "Maximum number of threads: " << max_threads << std::endl;

    return 0;
}