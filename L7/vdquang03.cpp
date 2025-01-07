#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();

        #pragma omp master
        {
            printf("Chỉ luồng chính (master thread) thực hiện.\n");
            printf("Luồng master là: %d\n", thread_id);

        }

        printf("Luồng %d đã được tạo.\n", thread_id);
    }

    return 0;
}