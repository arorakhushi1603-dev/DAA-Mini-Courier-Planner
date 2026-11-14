# Mini-Courier Planner — DAA Capstone

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**University:** K.R. Mangalam University, Gurugram  
**Language:** Python 3 (standard library only)

## 1. Problem overview
The application simulates a courier company. It sorts incoming parcels by urgency, chooses a high-value subset that fits the vehicle's weight capacity, and creates a delivery tour over a weighted road network.

## 2. Algorithms used
| Requirement | Algorithm | Purpose |
|---|---|---|
| Parcel prioritization | Merge Sort | Ascending deadline, then descending priority |
| Box filling | 0/1 Knapsack DP | Maximize total parcel value under capacity |
| Shortest path | Dijkstra with min-heap | Find minimum road distance |
| Overall tour | Nearest-Neighbour TSP approximation | Visit all selected destinations and return to depot |

## 3. Project structure
```text
Mini_Courier_Planner/
├── main.py
├── data/
│   ├── parcels.csv
│   └── roads.csv
├── outputs/
├── README.md
├── REPORT.md
└── TESTING.md
```

## 4. Run the program
1. Install Python 3.9 or newer.
2. Extract the project ZIP.
3. Open a terminal inside `Mini_Courier_Planner`.
4. Run:
   ```bash
   python main.py
   ```
5. Optional custom input:
   ```bash
   python main.py --parcels data/parcels.csv --edges data/roads.csv --capacity 15 --depot Depot
   ```

No third-party package is required for the main application.

## 5. Input format

### parcels.csv
- `id`: unique parcel identifier
- `destination`: delivery node in the road graph
- `weight`: parcel weight (integer units)
- `value`: business value / reward
- `deadline`: delivery deadline rank (smaller means more urgent)
- `priority`: priority score (larger means more important)

### roads.csv
- `from`, `to`: connected locations
- `distance`: non-negative road distance

Roads are treated as undirected. Add both directions only if you modify `load_graph` to use a directed graph.

## 6. Design decisions and assumptions
- The vehicle has one fixed maximum weight capacity.
- A parcel is indivisible and can be selected at most once.
- The knapsack objective is maximum total value; deadline and priority determine sorting order and are not extra knapsack constraints.
- If several parcels share a destination, the courier visits that destination once.
- Road distances are non-negative, as required by Dijkstra.
- The tour starts and ends at the depot.
- Nearest-neighbour is a heuristic. It is fast and practical but does not guarantee the globally shortest TSP tour.

## 7. Complexity
Let `n` be the number of parcels, `W` the vehicle capacity, `V` the number of graph vertices, `E` the number of road edges, and `k` the number of distinct selected destinations.

- Merge Sort: `O(n log n)` time; `O(n)` auxiliary space.
- 0/1 Knapsack: `O(nW)` time and `O(nW)` space for the full reconstruction table.
- Dijkstra with a binary heap: `O((V+E) log V)` time and `O(V+E)` graph storage.
- Nearest-Neighbour tour: runs shortest-path calculations between successive stops; with this implementation, approximately `O(k(V+E) log V)` time.

## 8. Viva preparation
Be ready to explain:
1. Why Merge Sort is `O(n log n)` in best, average and worst cases.
2. Why the knapsack table has `n+1` rows and `W+1` columns.
3. Why 0/1 Knapsack differs from Fractional Knapsack.
4. Why Dijkstra cannot safely handle negative edge weights.
5. How the priority queue selects the next closest vertex.
6. Why nearest-neighbour TSP is an approximation and can miss the optimal tour.
7. How the algorithms are connected in the application.
8. What changes if the vehicle capacity, graph, or parcel list changes.

## 9. Submission checklist
- [ ] Run the program successfully.
- [ ] Test at least three vehicle capacities.
- [ ] Add screenshots of terminal output to your report.
- [ ] Include runtime measurements from repeated tests.
- [ ] Explain the assumptions and complexity.
- [ ] Upload the extracted project folder to GitHub or submit the ZIP as instructed.
