#include <iostream>
#include <vector>
#include <thread>
#include <omp.h>

using namespace std;

void processArray(int threadNum, vector<int> &a, int size) {
    int x = 0;
    printf("x=%d\n", x);
    
    for (int i = 0; i < size; ++i) {
        x = (x > a[i]) ? x : a[i];
        printf("x=%d, a[%d]=%d Thread:%d\n", x, i, a[i], threadNum);
    }

    printf("\nx=%d\n", x);
}

int main() {
    int n;
    double start_time = omp_get_wtime(); 
    cout << "Enter array size: ";
    cin >> n;
  
    vector<int> a(n);
    cout << "Enter elements: ";
    for(int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    #pragma omp parallel
    {
        int threadNum = omp_get_thread_num();
        processArray(threadNum, a, n);
    }

    cout << "Time: " << omp_get_wtime() - start_time << endl;
    return 0;
}