#include <iostream>
#include <pthread.h>

void *thread_function(void *arg)
{
    int thread_id = *(int *)arg;
    std::cout << "Xin chao ban! Toi dang o luong so: " << thread_id << std::endl;
    pthread_exit(NULL);
}

int main()
{
    pthread_t threads[4];
    int thread_ids[4] = {0, 1, 2, 3}; // Thread IDs from 0 to 3

    for (int i = 0; i < 4; i++)
    {
        int rc = pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]);
        if (rc)
        {
            std::cerr << "Error creating thread: " << rc << std::endl;
            return 1;
        }
    }

    for (int i = 0; i < 4; ++i)
        pthread_join(threads[i], NULL); // Wait for threads to complete

    return 0;
}