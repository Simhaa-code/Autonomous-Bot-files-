import heapq
import folium
import webbrowser
import os

# -----------------------------------------
# Graph (Road Network)
# -----------------------------------------
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

# -----------------------------------------
# Coordinates (Replace with your campus)
# -----------------------------------------

locations = {

    "Main Gate": (13.118832, 77.655538),

    "Library": (13.119087, 77.660292),

    "Parking": (13.118419, 77.657856),

    "Admin Block": (13.118128917332388, 77.65955234351041),

    "Canteen": (13.119087, 77.660292)

}

# -----------------------------------------
# Dijkstra Algorithm
# -----------------------------------------

def dijkstra(graph, start, destination):

    distances = {}
    previous = {}

    for node in graph:
        distances[node] = float("inf")
        previous[node] = None

    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbour, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbour]:

                distances[neighbour] = distance

                previous[neighbour] = current_node

                heapq.heappush(priority_queue, (distance, neighbour))

    path = []

    node = destination

    while node is not None:

        path.append(node)

        node = previous[node]

    path.reverse()

    return path, distances[destination]


# -----------------------------------------
# Display Locations
# -----------------------------------------

print("\nAvailable Locations\n")

for place in graph:
    print(place)

print()

# -----------------------------------------
# User Input
# -----------------------------------------

start = input("Enter Starting Location : ")

destination = input("Enter Destination : ")

if start not in graph:

    print("Invalid Start Location")
    exit()

if destination not in graph:

    print("Invalid Destination")
    exit()

# -----------------------------------------
# Find Shortest Path
# -----------------------------------------

path, distance = dijkstra(graph, start, destination)

print("\nShortest Route\n")

for p in path:
    print(p)

print("\nTotal Distance =", distance, "meters")

# -----------------------------------------
# Create Folium Map
# -----------------------------------------

latitudes = [coord[0] for coord in locations.values()]
longitudes = [coord[1] for coord in locations.values()]

center = [
    sum(latitudes) / len(latitudes),
    sum(longitudes) / len(longitudes)
]

m = folium.Map(
location=center,
zoom_start=18,
tiles="OpenStreetMap"
)  
# -----------------------------------------
# Add Markers
# -----------------------------------------

for place, coordinate in locations.items():

    color = "blue"

    if place == start:
        color = "green"

    elif place == destination:
        color = "red"

    folium.Marker(
        coordinate,
        popup=place,
        icon=folium.Icon(color=color)
    ).add_to(m)

# -----------------------------------------
# Draw Route
# -----------------------------------------

route_coordinates = []

for point in path:

    route_coordinates.append(locations[point])

folium.PolyLine(
    route_coordinates,
    color="blue",
    weight=6,
    opacity=0.8
).add_to(m)

# -----------------------------------------
# Add Car Marker
# -----------------------------------------

folium.Marker(
    locations[start],
    popup="Car Starting Position",
    icon=folium.Icon(color="orange", icon="car", prefix="fa")
).add_to(m)

# -----------------------------------------
# Save Map
# -----------------------------------------

filename = "college_navigation_map.html"

m.save(filename)

print("\nMap Saved Successfully!")

print("File :", filename)

# -----------------------------------------
# Automatically Open Browser
# -----------------------------------------

webbrowser.open('file://' + os.path.realpath(filename))