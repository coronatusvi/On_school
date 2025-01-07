#include <stdio.h>
#include <omp.h>

int main() {
    int original_value = 10;

    #pragma omp parallel for lastprivate(original_value)
    for (int i = 0; i < 5; i++) {
        original_value = i;
        printf("Luồng %d: Giá trị i = %d, original_value = %d\n", omp_get_thread_num(), i, original_value);
    }

    printf("Giá trị original_value sau vòng lặp = %d\n", original_value);

    return 0;
}