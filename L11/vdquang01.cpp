#include <iostream>
#include <pthread.h>

int dem = 0;
pthread_mutex_t mutex;

void *count(void *arg)
{
    for (int i = 0; i < 1000000; i++)
    {
        pthread_mutex_lock(&mutex);
        dem++;
        pthread_mutex_unlock(&mutex);
    }
    pthread_exit(NULL);
}

int main()
{
    pthread_t tid[4];
    pthread_mutex_init(&mutex, NULL);

    for (int i = 0; i < 4; i++)
    {
        pthread_create(&tid[i], NULL, count, NULL);
    }

    for (int i = 0; i < 4; i++)
    {
        pthread_join(tid[i], NULL);
    }

    printf("Dem=%d\n", dem);

    pthread_mutex_destroy(&mutex);

    pthread_exit(NULL);
    return 0;
}