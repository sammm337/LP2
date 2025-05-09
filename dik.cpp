#include <iostream>
#include <vector>
#include <queue>
#include <climits>
using namespace std;

vector<int> dijkstra(vector<vector<pair<int, int>>>& adj, int V, int src) {
    vector<int> dist(V, INT_MAX);
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        for (auto& [v, weight] : adj[u]) {
            if (dist[v] > dist[u] + weight) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    int V, E, src;
    cout << "Enter number of vertices and edges: ";
    cin >> V >> E;
    vector<vector<pair<int, int>>> adj(V);

    cout << "Enter edges (u v weight):\n";
    for (int i = 0; i < E; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        // adj[v].push_back({u, w}); for undirected graph uncomment this line
    }

    cout << "Enter source vertex: ";
    cin >> src;

    vector<int> dist = dijkstra(adj, V, src);
    cout << "Shortest distances from node " << src << ":\n";
    for (int i = 0; i < V; i++)
        cout << "Node " << i << " : " << dist[i] << endl;
    return 0;
}

// Greedy Concept:
// At every step, it chooses the node with the smallest tentative distance (greedy) and updates distances to its neighbors — assumes shorter paths found early are best.

// Time Complexity:
//     O((V + E) log V) with min-heap
// Space Complexity:
//     O(V)