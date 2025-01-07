#include<iostream>
#include<omp.h>

int main () {
    #pragma omp parallel for ordered
    for (int i = 0; i <= 16; i++) {
        #pragma omp ordered
        std::cout << "Thread " << omp_get_thread_num() << " is working on " << i << std::endl;
    }
}   