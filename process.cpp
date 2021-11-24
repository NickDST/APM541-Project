#include <iostream>
#include <vector>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <math.h>       /* time */

using namespace std;


float uniform(){
    float u = (float) rand()/RAND_MAX;
    return u;
}

float exponential(float u, float mu){
    float s = (float) -log(u)/mu;
    return s;
}


int rnd_sel_neighbor(std::vector<int>& adj, int x){
    float u = uniform();
    int y_idx = int(floor((adj.size()-1) * u));
    int y = adj[y_idx];
    return y;
}

void print_cmap(int col[], int N){
    int infected_cnt = 0;
    int normal_cnt = 0;
    int alerted_cnt = 0;

    for(int i = 0; i < N; i++){
        if(col[i] == 0){
            normal_cnt++;
        }else if(col[i] == 1){
            infected_cnt++;
        }else{
            alerted_cnt++;
        }
    }

//    cout << "Infected: " << infected_cnt << " || Normal: " << normal_cnt  << " || Alerted: " << alerted_cnt << endl;

//    this is the CSV version
    cout << infected_cnt << "," << normal_cnt  << "," << alerted_cnt << "," << "ID11" << endl;
}


int main() {

    int N = 4039;
    // creating an array of vectors as the adjacency list for the graph
    vector<int> G[N];

    std::string networkName = "data/graph_social.txt";
    std::cout << "Loading in Graph..." << std::endl;

    FILE *file;
    file = fopen(networkName.c_str(), "r");
    int u_id, v_id;

    if (file) {

        for (int i = 0; i < 88234; i++) {
            fscanf(file, "%d", &u_id);
            fscanf(file, "%d", &v_id);
            G[u_id].push_back(v_id);
            G[v_id].push_back(u_id);
        }

    }



    std::cout << "Starting Sim..." << std::endl;

    // Initializing variables and loading the simulation
    int colors[N];
    float bI = 4;
    float dI = 1;
    float bA = 1;
    float dA = 1;
    float t;
    float max_t = 10000;
    int num_trials = 1;

    float U;
    int site;
    float u;
    int y;

    time_t amorce;
    time(&amorce);
    srand(amorce); //setting the seed for a random number


    for (int trial = 0; trial < num_trials; trial++) {

        //resetting the parameters, the time and the colors of the graph
        t = 0;
        //setting all to empty
        for (int i = 0; i < N; i++) {
            colors[i] = 0;
        }


        //setting one of the colors to be infected, let us set it to the least connected node
        //least 10 connected nodes
        colors[1096] = 1;
        colors[292] = 1;
        colors[210] = 1;
        colors[1834] = 1;
        colors[209] = 1;
        colors[4024] = 1;
        colors[3451] = 1;
        colors[3453] = 1;
        colors[550] = 1;
        colors[1466] = 1;


        //top 10 most connected
//        colors[107] = 1;
//        colors[1684] = 1;
//        colors[1912] = 1;
//        colors[3437] = 1;
//        colors[0] = 1;
//        colors[2543] = 1;
//        colors[2347] = 1;
//        colors[1888] = 1;
//        colors[1800] = 1;
//        colors[1663] = 1;
        float curr_t = 0;

        while (t < max_t) {

            if(t > curr_t){
                cout << curr_t << endl;
                curr_t += 1000;
            }

            u = uniform();
            t = t + exponential(u, (bI + dI + bA + dA) * N);
            site = floor((N - 1) * u);

            if (colors[site] == 1) {
                U = uniform() * (bI + dI);

                if (U < dI) {
                    colors[site] = 2;
                } else {
                    y = rnd_sel_neighbor(G[site], site);
                    if (colors[y] == 2) {
                        colors[site] = 2;
                    } else {
                        colors[y] = 1;
                    }
                }


            } else if (colors[site] == 2) {
                U = uniform() * (bA + dA);
                if (U < dA) {
                    colors[site] = 0;
                } else {
                    y = rnd_sel_neighbor(G[site], site);
                    colors[y] = 2; // set the neighbor to be alerted
                }
            }
        }

        print_cmap(colors, N);
}
    cout << "Finished" << endl;

    return 0;
}




