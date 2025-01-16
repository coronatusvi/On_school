#include <iostream>
#include <pthread.h>
#include <vector>

struct ThreadData
{
    int start;
    int end;
    long long partial_sum;
};

void *thread_sum_function(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    long long local_sum = 0;
    for (int i = data->start; i <= data->end; ++i)
    {
        local_sum += i;
    }
    data->partial_sum = local_sum;
    pthread_exit(NULL);
}

int main()
{
    int n = 1000000;
    int num_threads = 4;
    std::vector<long long> partial_sums(num_threads, 0);
    pthread_t threads[num_threads];
    ThreadData thread_data[num_threads];

    int chunk_size = n / num_threads;
    long long total_sum = 0;

    for (int i = 0; i < num_threads; ++i)
    {
        thread_data[i].start = i * chunk_size + 1;
        thread_data[i].end = (i == num_threads - 1) ? n : (i + 1) * chunk_size;
        int rc = pthread_create(&threads[i], NULL, thread_sum_function, &thread_data[i]);
        if (rc)
        {
            std::cerr << "Error creating thread: " << rc << std::endl;
            return 1;
        }
    }

    for (int i = 0; i < num_threads; ++i)
    {
        pthread_join(threads[i], NULL);
        total_sum += thread_data[i].partial_sum;
    }

    std::cout << "Total sum = " << total_sum << std::endl;

    return 0;
}