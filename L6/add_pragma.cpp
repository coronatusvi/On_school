#include<iostream>
#include<omp.h>

using namespace std;

int main () {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int sum = 0;
    for (int i = 0; i <= 100; i++) {
        sum += i;
    }
    cout << "Tuan tu: " << sum << endl;

    // omp_set_num_threads(4);
    
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i <= 100; i++) {
        sum += i;
    }
    cout << "Song song: " << sum << endl;
    return 0;
}   