#include <iostream>
#include <vector>
#include <omp.h>
#include <chrono>
#include <iomanip>


void heat_distribution_parallel(int N, int t_steps, int num_threads, std::vector<std::vector<double>>& final_grid, double& elapsed_time) {
     std::vector<std::vector<double>> U(N, std::vector<double>(N, 0.0)); 
     std::vector<std::vector<double>> U_new(N, std::vector<double>(N, 0.0)); 

    for (int i = 0; i < N; ++i) {
        U[0][i] = 100.0;
        U[N - 1][i] = 100.0;
        U[i][0] = 100.0;
        U[i][N - 1] = 100.0;
    }


    auto start_time = std::chrono::high_resolution_clock::now();

    for (int t = 0; t < t_steps; ++t) {
        #pragma omp parallel for num_threads(num_threads) collapse(2)
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                 if (i == 0 || i == N - 1 || j == 0 || j == N - 1) {
                    U_new[i][j] = U[i][j];
                 } else{
                     U_new[i][j] = (4 * U[i][j] + U[i - 1][j] + U[i + 1][j] + U[i][j - 1] + U[i][j + 1]) / 8;
                 }

            }
        }
       U = U_new;
    }


     auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(end_time - start_time);

     final_grid = U;
     elapsed_time = duration.count();

}


int main() {
    int N = 128;
    int t_steps = 1000;

    std::vector<std::vector<double>> U_parallel;
    double elapsed_time_parallel;
    
    std::cout << std::fixed << std::setprecision(4);

    for (int num_threads = 1; num_threads <= 16; num_threads++) {

        heat_distribution_parallel(N, t_steps, num_threads, U_parallel, elapsed_time_parallel);

        std::cout << "Parallel Simulation Results with " << num_threads << " Threads:" << std::endl;
        std::cout << "    Elapsed Time: " << elapsed_time_parallel << " seconds" << std::endl;
    }

    return 0;
}   