#include <stdio.h>
#include <omp.h>

int main() {
    int original_value = 10;

    #pragma omp parallel firstprivate(original_value)
    {
        int thread_id = omp_get_thread_num();
        original_value += thread_id;
        printf("Luồng %d: Giá trị = %d\n", thread_id, original_value);
    }
    printf("Giá trị gốc (ngoài vùng song song) = %d\n", original_value);

    return 0;
}