#include <iostream>
#include <omp.h>

int main() {
    int n;
    std::cout << "Nhập n: ";
    std::cin >> n;

    long long total_sum = 0;
    omp_lock_t lock;
    omp_init_lock(&lock);

    #pragma omp parallel
    {
        long long private_sum = 0;
        int id = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = n / num_threads;
        int start = id * chunk_size + 1;
        int end = (id == num_threads - 1) ? n : start + chunk_size - 1;

        for (int i = start; i <= end; ++i) {
            private_sum += i;
        }

        omp_set_lock(&lock);
        total_sum += private_sum;
        omp_unset_lock(&lock);
    }

    omp_destroy_lock(&lock);
    std::cout << "Tổng S = " << total_sum << std::endl;
    return 0;
}
