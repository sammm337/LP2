#include <iostream>
#include <queue>
#include <vector>
using namespace std;

const int MAX = 100;
int adj[MAX][MAX]; // Adjacency matrix
bool visited[MAX];
int n; // Number of nodes

void BFS(int start) {
    fill(visited, visited + n, false);
    queue<int> q;
    visited[start] = true;
    q.push(start);

    cout << "BFS starting from node " << start << ": ";
    while (!q.empty()) {
        int node = q.front();
        q.pop();
        cout << node << " ";

        for (int i = 0; i < n; ++i) {
            if (adj[node][i] && !visited[i]) {
                visited[i] = true;
                q.push(i);
            }
        }
    }
    cout << endl;
}

void DFS(int node) {
    visited[node] = true;
    cout << node << " ";

    for (int i = 0; i < n; ++i) {
        if (adj[node][i] && !visited[i]) {
            DFS(i);
        }
    }
}

int main() {
    int edges;
    cout << "Enter number of nodes and edges: ";
    cin >> n >> edges;

    // Initialize adjacency matrix
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            adj[i][j] = 0;

    cout << "Enter edges (u v):\n";
    for (int i = 0; i < edges; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u][v] = 1;
        adj[v][u] = 1; // For undirected graph
    }

    int start;
    cout << "Enter starting node: ";
    cin >> start;

    BFS(start);

    fill(visited, visited + n, false); // Reset visited for DFS
    cout << "DFS starting from node " << start << ": ";
    DFS(start);
    cout << endl;

    return 0;
}
