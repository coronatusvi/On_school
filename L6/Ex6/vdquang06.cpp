#include <iostream>
#include <vector>
#include <climits>
#include <omp.h>
#include <iomanip> 

using namespace std;

int minNonZero(const vector<int>& arr) {
    int n = arr.size();
    if (n == 0) return -1;
    
    int min_val = INT_MAX;
    bool found_non_zero = false;
    double start_time, end_time;
   
    start_time = omp_get_wtime();
    #pragma omp parallel for reduction(min:min_val)
    for(int i = 0; i < n; ++i){
        if(arr[i] > 0) {
            found_non_zero = true;
            min_val = min(min_val, arr[i]);
        }
    }
     end_time = omp_get_wtime();
    double seconds = end_time - start_time;

    cout << "Time: " << fixed << setprecision(3) << seconds << "s" << endl;


    return found_non_zero ? min_val : -1;
}

int main() {
    vector<int> arr1 = {0, 2, 5, 1, 0, 3};
    cout << "arr1: " << minNonZero(arr1) << endl;

    vector<int> arr2 = {0, 0, 0, 0};
    cout << "arr2: " << minNonZero(arr2) << endl;

    vector<int> arr3 = {};
    cout << "arr3: " << minNonZero(arr3) << endl;

    vector<int> arr4 = {2, 4, 6, 1, 3};
    cout << "arr4: " << minNonZero(arr4) << endl;
    
    return 0;
}