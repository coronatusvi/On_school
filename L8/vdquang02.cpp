#include <iostream>
#include <omp.h>

using namespace std;

int main()
{
    int n;
    cout << "Nhap n: ";
    cin >> n;

    long long total_sum = 0;

#pragma omp parallel
    {
        long long private_sum = 0;
        int id = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = n / num_threads;
        int start = id * chunk_size + 1;
        int end = (id == num_threads - 1) ? n : start + chunk_size - 1;

        for (int i = start; i <= end; i++)
        {
            private_sum += i;
        }

#pragma omp critical
        {
            total_sum += private_sum;
        }
    }

    cout << "Tong S = " << total_sum << endl;
    return 0;
}