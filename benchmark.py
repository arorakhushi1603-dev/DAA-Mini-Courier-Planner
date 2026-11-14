"""Generate runtime data and a chart for Merge Sort and 0/1 Knapsack."""
import csv
import random
import time
from pathlib import Path
import matplotlib.pyplot as plt
from main import merge_sort_parcels, knapsack_01

random.seed(42)
sizes = [10, 25, 50, 100, 200, 400]
capacity = 100
rows = []

for n in sizes:
    parcels = [{
        "id": f"P{i:04d}", "destination": "A",
        "weight": random.randint(1, 15),
        "value": random.randint(10, 200),
        "deadline": random.randint(1, 30),
        "priority": random.randint(1, 5)
    } for i in range(n)]

    sort_samples, dp_samples = [], []
    for _ in range(5):
        start = time.perf_counter()
        merge_sort_parcels(parcels)
        sort_samples.append(time.perf_counter() - start)

        start = time.perf_counter()
        knapsack_01(parcels, capacity)
        dp_samples.append(time.perf_counter() - start)

    rows.append((n, capacity, sum(sort_samples)/5, sum(dp_samples)/5))

out = Path("outputs")
out.mkdir(exist_ok=True)
with open(out / "benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["parcel_count", "capacity", "merge_sort_avg_seconds", "knapsack_avg_seconds"])
    writer.writerows(rows)

plt.figure()
plt.plot([r[0] for r in rows], [r[2] for r in rows], marker="o", label="Merge Sort")
plt.plot([r[0] for r in rows], [r[3] for r in rows], marker="s", label="0/1 Knapsack DP")
plt.xlabel("Number of parcels (n)")
plt.ylabel("Average runtime (seconds)")
plt.title(f"Mini-Courier Planner: Runtime Comparison (capacity={capacity})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(out / "runtime_comparison.png", dpi=160)
print("Saved outputs/benchmark_results.csv")
print("Saved outputs/runtime_comparison.png")
for n, cap, sort_t, dp_t in rows:
    print(f"n={n:>3}, W={cap}: Merge Sort={sort_t:.8f}s, Knapsack={dp_t:.8f}s")
