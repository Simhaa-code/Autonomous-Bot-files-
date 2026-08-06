import heapq

# -----------------------------
# College Map (Graph)
# -----------------------------
graph = {
    "Main Gate": {
        "Library": 100,
        "Parking": 80
    },

    "Library": {
        "Main Gate": 100,
        "Admin Block": 120,
        "Canteen": 60
    },

    "Parking": {
        "Main Gate": 80,
        "Admin Block": 90
    },

    "Admin Block": {
        "Library": 120,
        "Parking": 90,
        "Canteen": 70
    },

    "Canteen": {
        "Library": 60,
        "Admin Block": 70
    }
}


# -----------------------------
# Dijkstra Algorithm
# -----------------------------
def dijkstra(graph, start, destination):

    # Store shortest distances
    distances = {}

    # Store previous node
    previous = {}

    # Initially every node has infinite distance
    for node in graph:
        distances[node] = float("inf")
        previous[node] = None

    distances[start] = 0

    # Priority Queue
    pq = [(0, start)]

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        # Ignore old entries
        if current_distance > distances[current_node]:
            continue

        # Check all neighbours
        for neighbour, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbour]:

                distances[neighbour] = distance

                previous[neighbour] = current_node

                heapq.heappush(pq, (distance, neighbour))

    # -----------------------------
    # Reconstruct shortest path
    # -----------------------------
    path = []

    node = destination

    while node is not None:

        path.append(node)

        node = previous[node]

    path.reverse()

    return path, distances[destination]


# -----------------------------
# Show Available Locations
# -----------------------------
print("\nAvailable Locations:\n")

for place in graph:
    print("-", place)

print()

# -----------------------------
# User Input
# -----------------------------
start = input("Enter Starting Location : ")

destination = input("Enter Destination : ")

# Check validity
if start not in graph:
    print("\nInvalid Starting Location")
    exit()

if destination not in graph:
    print("\nInvalid Destination")
    exit()

# -----------------------------
# Find Route
# -----------------------------
path, distance = dijkstra(graph, start, destination)

print("\nShortest Route")

for location in path:
    print(location)

print("\nTotal Distance =", distance, "meters")