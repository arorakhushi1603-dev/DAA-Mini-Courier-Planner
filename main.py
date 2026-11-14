"""
Mini-Courier Planner
DAA Capstone | ETCCDA302
Algorithms: Merge Sort, 0/1 Knapsack (Dynamic Programming),
Dijkstra's Shortest Path, Nearest-Neighbour TSP Approximation.

Run:
    python main.py
    python main.py --parcels data/parcels.csv --edges data/roads.csv --capacity 15
"""
import argparse
import csv
import heapq
import time
from pathlib import Path


def load_parcels(path):
    parcels = []
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            parcels.append({
                "id": row["id"],
                "destination": row["destination"],
                "weight": int(row["weight"]),
                "value": int(row["value"]),
                "deadline": int(row["deadline"]),
                "priority": int(row["priority"]),
            })
    return parcels


def load_graph(path):
    graph = {}
    with open(path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            u, v, distance = row["from"], row["to"], float(row["distance"])
            graph.setdefault(u, {})[v] = distance
            graph.setdefault(v, {})[u] = distance
    return graph


def merge_sort_parcels(parcels):
    """Stable merge sort: earlier deadline, then higher priority, then ID."""
    if len(parcels) <= 1:
        return parcels[:]
    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])
    result, i, j = [], 0, 0

    def key(p):
        return (p["deadline"], -p["priority"], p["id"])

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def knapsack_01(parcels, capacity):
    """
    0/1 Knapsack DP.
    Each parcel is either selected once or not selected.
    Returns selected parcels and the maximum total value.
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = parcels[i - 1]["weight"]
        value = parcels[i - 1]["value"]
        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]
            if weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    value + dp[i - 1][cap - weight]
                )

    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            cap -= parcel["weight"]

    selected.reverse()
    return selected, dp[n][capacity], dp


def dijkstra(graph, source):
    """Returns shortest distances and predecessor map from source."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    if source not in graph:
        raise ValueError(f"Source location '{source}' is not in the road graph.")

    distances[source] = 0
    pq = [(0, source)]

    while pq:
        current_distance, u = heapq.heappop(pq)
        if current_distance != distances[u]:
            continue
        for v, weight in graph[u].items():
            candidate = current_distance + weight
            if candidate < distances[v]:
                distances[v] = candidate
                previous[v] = u
                heapq.heappush(pq, (candidate, v))
    return distances, previous


def reconstruct_path(previous, target):
    if target not in previous:
        return []
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = previous[node]
    return list(reversed(path))


def nearest_neighbour_tsp(graph, start, destinations):
    """
    Nearest-neighbour TSP approximation.
    Uses Dijkstra distances as metric edge costs, then returns to start.
    Each distinct destination is visited once.
    """
    stops = list(dict.fromkeys(destinations))
    if start not in graph:
        raise ValueError(f"Starting location '{start}' is not in the graph.")
    unknown = [s for s in stops if s not in graph]
    if unknown:
        raise ValueError(f"Unknown destination(s): {', '.join(unknown)}")

    route = [start]
    total_distance = 0.0
    current = start
    remaining = set(stops)
    shortest_cache = {}

    while remaining:
        distances, previous = dijkstra(graph, current)
        reachable = [(distances[s], s) for s in remaining
                     if distances[s] != float("inf")]
        if not reachable:
            raise ValueError("Some delivery points are disconnected from the route.")
        distance, next_stop = min(reachable, key=lambda item: (item[0], item[1]))
        total_distance += distance
        route.append(next_stop)
        remaining.remove(next_stop)
        current = next_stop

    distances, _ = dijkstra(graph, current)
    if distances[start] == float("inf"):
        raise ValueError("The route cannot return to the depot.")
    total_distance += distances[start]
    route.append(start)
    return route, total_distance


def timed_call(function, *args):
    start = time.perf_counter()
    result = function(*args)
    return result, time.perf_counter() - start


def print_parcels(title, parcels):
    print(f"\n{title}")
    print("-" * len(title))
    if not parcels:
        print("No parcels.")
        return
    print(f"{'ID':<8}{'Destination':<16}{'Weight':>8}{'Value':>8}{'Deadline':>10}{'Priority':>10}")
    for p in parcels:
        print(f"{p['id']:<8}{p['destination']:<16}{p['weight']:>8}{p['value']:>8}"
              f"{p['deadline']:>10}{p['priority']:>10}")


def run(parcels_path, roads_path, capacity, depot):
    parcels = load_parcels(parcels_path)
    graph = load_graph(roads_path)

    sorted_result, sort_time = timed_call(merge_sort_parcels, parcels)
    print_parcels("PHASE 2A: PARCELS SORTED BY DEADLINE / PRIORITY", sorted_result)

    (selected, total_value, dp), knapsack_time = timed_call(
        knapsack_01, sorted_result, capacity
    )
    print_parcels("PHASE 2B: OPTIMAL PARCELS SELECTED FOR THE TRIP", selected)
    total_weight = sum(p["weight"] for p in selected)
    print(f"\nVehicle capacity : {capacity}")
    print(f"Selected weight  : {total_weight}")
    print(f"Unused capacity  : {capacity - total_weight}")
    print(f"Total parcel value: {total_value}")

    destinations = [p["destination"] for p in selected]
    # A destination shared by multiple parcels is visited only once.
    route, route_distance = nearest_neighbour_tsp(graph, depot, destinations)
    print("\nPHASE 3A: DELIVERY ROUTE (NEAREST-NEIGHBOUR TSP)")
    print(" -> ".join(route))
    print(f"Total route distance: {route_distance:.2f} distance units")

    print("\nPHASE 3B: DIJKSTRA SHORTEST-PATH DETAILS")
    for destination in dict.fromkeys(destinations):
        distances, previous = dijkstra(graph, depot)
        path = reconstruct_path(previous, destination)
        print(f"{depot} -> {destination}: {' -> '.join(path)} "
              f"(distance = {distances[destination]:.2f})")

    print("\nPHASE 4: RUNTIME SUMMARY")
    print(f"{'Algorithm':<30}{'Runtime (seconds)':>20}")
    print("-" * 50)
    print(f"{'Merge Sort':<30}{sort_time:>20.8f}")
    print(f"{'0/1 Knapsack DP':<30}{knapsack_time:>20.8f}")
    print("\nComplexity reference:")
    print("Merge Sort: O(n log n) time, O(n) auxiliary space")
    print("0/1 Knapsack: O(nW) time and O(nW) DP-table space")
    print("Dijkstra (binary heap): O((V + E) log V) time")
    print("Nearest Neighbour TSP: O(k * Dijkstra) in this implementation; "
          "heuristic, not guaranteed optimal")


def main():
    parser = argparse.ArgumentParser(description="Mini-Courier Planner")
    parser.add_argument("--parcels", default="data/parcels.csv")
    parser.add_argument("--edges", default="data/roads.csv")
    parser.add_argument("--capacity", type=int, default=15)
    parser.add_argument("--depot", default="Depot")
    args = parser.parse_args()

    if args.capacity < 0:
        parser.error("--capacity must be non-negative")
    run(args.parcels, args.edges, args.capacity, args.depot)


if __name__ == "__main__":
    main()
