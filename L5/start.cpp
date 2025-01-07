#include <iostream>
#include <omp.h>

int main() {
    int i, s=0;

    #pragma omp parallel for shared(s) private(i) schedule(static, 2)
    for (i=1; i<=20; i++) {      
        std::cout << "Thread " << omp_get_thread_num() << " is working on " << i << std::endl;
        s += i;
    }

    std::cout << "Sum is: " << s << std::endl;
    return 0;   
}