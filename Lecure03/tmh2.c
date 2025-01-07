#include<stdio.h>
#include<omp.h>

int main(){
    printf("Trước khi vào vùng song song: Số lượng lõi: %d\n", omp_get_num_procs());

    #pragma omp parallel
    {
        printf("Từ luồng %d trong tổng số %d luồng.\n", omp_get_thread_num(), omp_get_num_threads());
    }

    printf("Sau khi ra vùng song song.\n");
    return 0;
}