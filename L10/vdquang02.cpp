#include <iostream>
#include <pthread.h>
#include <string>

struct ThreadData
{
    std::string message;
};

void *thread_function(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    std::cout << data->message << std::endl;
    pthread_exit(NULL);
}

int main()
{
    pthread_t threads[4];
    ThreadData thread_data[4];

    std::string messages[4] = {
        "Chao ban tu Viet Nam",
        "Chao ban tu Cu Ba",
        "Chao ban tu USA",
        "Chao ban tu Uc"};

    for (int i = 0; i < 4; ++i)
    {
        thread_data[i].message = messages[i];
        int rc = pthread_create(&threads[i], NULL, thread_function, &thread_data[i]);
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