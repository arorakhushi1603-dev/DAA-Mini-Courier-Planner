# DAA Capstone Report: Mini-Courier Planner

**K.R. Mangalam University, Gurugram, Haryana**  
**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**Faculty:** Dr. Shweta Agarwal  
**Student Name:** ____________________  
**Roll Number:** ____________________  
**Submission Date:** ____________________

## Abstract
The Mini-Courier Planner is a Python prototype that combines sorting, dynamic programming, graph processing and approximation techniques to support courier delivery planning. It prioritizes parcels, selects a feasible high-value set under a vehicle capacity, computes shortest paths and constructs a delivery tour.

## Phase 1 — Courier Problem Design and Planning
### Problem definition
Given a set of parcels, a vehicle capacity and a weighted road graph, select parcels whose total weight does not exceed capacity while maximizing their total value. Then visit the selected parcel destinations, beginning and ending at the depot.

### Data design
Each parcel contains: parcel ID, destination, weight, value, deadline and priority. The road network is an undirected weighted adjacency-list graph. Each edge stores the distance between two connected locations.

### Workflow
1. Read parcel and road-network CSV files.
2. Sort parcels by earliest deadline, then highest priority.
3. Apply 0/1 Knapsack DP to select parcels.
4. Use Dijkstra to compute shortest paths.
5. Use nearest-neighbour TSP approximation to order the selected destinations.
6. Display the route, selected parcels, capacity usage and runtime.

## Phase 2 — Package Prioritization and Box Filling
### Merge Sort
Merge Sort recursively divides the parcel list into halves, sorts each half and merges the halves. The comparison key is `(deadline ascending, priority descending, parcel ID ascending)`. This ensures urgent parcels appear first and higher-priority parcels break deadline ties.

**Time complexity:** `O(n log n)`  
**Auxiliary space:** `O(n)`

### 0/1 Knapsack using Dynamic Programming
Let `DP[i][c]` represent the maximum value achievable using the first `i` parcels and capacity `c`.

\[
DP[i][c] =
egin{cases}
DP[i-1][c], & w_i > c \
\max(DP[i-1][c], v_i + DP[i-1][c-w_i]), & w_i \le c
\end{cases}
\]

The final cell `DP[n][W]` gives the maximum achievable value. Backtracking through the table identifies the selected parcels.

**Time complexity:** `O(nW)`  
**Space complexity:** `O(nW)`

## Phase 3 — Route Maker and Graph Processing
### Graph representation
The road network is stored as an adjacency list. Each location maps to its directly connected neighbours and the corresponding non-negative road distances.

### Dijkstra's Algorithm
Dijkstra uses a min-priority queue. It repeatedly extracts the unvisited node with the smallest tentative distance and relaxes its outgoing edges. The predecessor map is used to reconstruct a shortest path.

**Time complexity with a binary heap:** `O((V+E) log V)`  
**Important condition:** all edge weights must be non-negative.

### Nearest-Neighbour TSP Approximation
Starting at the depot, the algorithm repeatedly selects the nearest unvisited delivery destination based on shortest-path distance. After all destinations are visited, it returns to the depot. This is a heuristic and does not guarantee the optimal travelling-salesperson tour.

## Phase 4 — Performance Testing and Optimization
The application measures Merge Sort and Knapsack execution time with `time.perf_counter()`. For a stronger experiment, run the program several times with different parcel counts and capacities, record the average runtime, and plot the results.

| Test | Parcel count | Capacity | Expected validation |
|---|---:|---:|---|
| Small | 8 | 15 | Program completes and capacity is not exceeded |
| Medium | 50 | 50 | DP returns a feasible maximum-value selection |
| Large | 200 | 100 | Runtime increases as input size/capacity increases |

**Optimization observations:** use a heap for Dijkstra rather than scanning all vertices; use adjacency lists for sparse road networks; avoid recalculating shortest paths where caching is beneficial; and consider a one-dimensional DP array if memory is constrained (but retain reconstruction information if the selected parcel list is required).

## Phase 5 — Final Report and Demonstration
Insert genuine screenshots of:
1. Successful program execution.
2. Sorted parcel list.
3. Knapsack-selected parcels and capacity calculation.
4. Shortest-path output and final route.
5. Runtime summary and any benchmark chart.

### Conclusion
The project demonstrates how multiple algorithmic techniques can be integrated into a practical planning problem. Merge Sort prioritizes parcels, dynamic programming optimizes the load, Dijkstra finds shortest paths, and nearest-neighbour TSP creates an approximate delivery tour. The prototype is modular, uses CSV input and can be extended with real map data, delivery time windows and multiple vehicles.

### Limitations and future scope
The current model uses static road distances and one vehicle. Future improvements can include traffic-aware edge weights, multiple vehicles, delivery time windows, live GPS, route improvement using 2-opt, and a graphical user interface.
