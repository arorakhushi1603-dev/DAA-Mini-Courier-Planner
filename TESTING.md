# Testing and Evidence Log

Run `python main.py` from the project folder.

## Functional test cases
| Test | Input variation | Expected result |
|---|---|---|
| T1 | Default CSV, capacity 15 | Valid selected parcels; total weight <= 15 |
| T2 | Capacity 0 | No parcel selected; route is Depot only |
| T3 | Capacity 5 | Selected weight <= 5 |
| T4 | Increase capacity to 25 | Optimal value cannot be lower than capacity-15 result |
| T5 | Add a parcel with an earlier deadline | It appears earlier in sorted output |
| T6 | Add a disconnected destination | Program reports a clear route error |
| T7 | Add a negative road distance | Do not use; Dijkstra requires non-negative weights |

## Record your actual measurements
Do not invent runtime values. Run each test at least five times and record the average.

| Dataset | Parcels (n) | Capacity (W) | Merge Sort avg (s) | Knapsack avg (s) |
|---|---:|---:|---:|---:|
| Small | 8 | 15 | | |
| Medium | 50 | 50 | | |
| Large | 200 | 100 | | |

## Screenshot evidence
Save screenshots in this folder and name them:
- `outputs/01_execution.png`
- `outputs/02_sorted_parcels.png`
- `outputs/03_knapsack.png`
- `outputs/04_route.png`
- `outputs/05_runtime.png`

Screenshots must come from your own execution.
