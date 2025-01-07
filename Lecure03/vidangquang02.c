#include <stdio.h>
#include <omp.h>

int main() {
    printf("Trước khi vào vùng song song: Số lượng lõi: %d\n", omp_get_num_procs());

    #pragma omp parallel
    {
        printf("Từ luồng %d trong tổng số %d luồng.\n", omp_get_thread_num(), omp_get_num_threads());
    }

    printf("Sau khi ra vùng song song.\n");
    return 0;
}
// Result:
// Trước khi vào vùng song song: Số lượng lõi: 20
// Từ luồng 9 trong tổng số 20 luồng.
// Từ luồng 8 trong tổng số 20 luồng.
// Từ luồng 1 trong tổng số 20 luồng.
// Từ luồng 14 trong tổng số 20 luồng.
// Từ luồng 5 trong tổng số 20 luồng.
// Từ luồng 15 trong tổng số 20 luồng.
// Từ luồng 12 trong tổng số 20 luồng.
// Từ luồng 2 trong tổng số 20 luồng.
// Từ luồng 3 trong tổng số 20 luồng.
// Từ luồng 16 trong tổng số 20 luồng.
// Từ luồng 13 trong tổng số 20 luồng.
// Từ luồng 7 trong tổng số 20 luồng.
// Từ luồng 19 trong tổng số 20 luồng.
// Từ luồng 11 trong tổng số 20 luồng.
// Từ luồng 10 trong tổng số 20 luồng.
// Từ luồng 0 trong tổng số 20 luồng.
// Từ luồng 4 trong tổng số 20 luồng.
// Từ luồng 18 trong tổng số 20 luồng.
// Từ luồng 6 trong tổng số 20 luồng.
// Từ luồng 17 trong tổng số 20 luồng.
// Sau khi ra vùng song song.