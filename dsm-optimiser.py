import itertools
import streamlit as st

class DeliveryGraph:
    def __init__(self):
        self.locations = []
        self.graph = {}

    def add_location(self, location):
        self.locations.append(location)
        self.graph[location] = {}

    def add_distance(self, from_location, to_location, distance):
        self.graph[from_location][to_location] = distance
        self.graph[to_location][from_location] = distance  

def calculate_route_distance(route, graph):
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += graph.graph[route[i]][route[i+1]]
    return total_distance

def find_best_route(graph, start_location):
    locations = graph.locations.copy()
    locations.remove(start_location)

    best_route = None
    min_distance = float('inf')

    for perm in itertools.permutations(locations):
        route = [start_location] + list(perm)
        distance = calculate_route_distance(route, graph)

        if distance < min_distance:
            min_distance = distance
            best_route = route

    return best_route, min_distance

# Streamlit UI
st.title("Delivery Route Optimizer")

num_locations = st.number_input("Enter the number of delivery locations:", min_value=2, step=1)

graph = DeliveryGraph()

# Add locations
locations = []
for i in range(num_locations):
    location = st.text_input(f"Enter delivery location {i + 1}:", key=f"loc_{i}")
    if location:
        graph.add_location(location)
        locations.append(location)

# Add distances
st.write("Enter the distance between each pair of locations:")
for i in range(len(locations)):
    for j in range(i + 1, len(locations)):
        if locations[i] and locations[j]:
            distance = st.number_input(
                f"Distance between {locations[i]} and {locations[j]}:",
                min_value=0.1,  # Allows decimal values
                step=0.1,
                format="%.2f",
                key=f"dist_{i}_{j}"
            )
            graph.add_distance(locations[i], locations[j], distance)

# Select starting location
if locations:
    start_location = st.selectbox("Select the starting location:", locations)

    if st.button("Find Best Route"):
        best_route, min_distance = find_best_route(graph, start_location)
        st.success(f"Best Route: {' -> '.join(best_route)}")
        st.info(f"Total Distance: {min_distance:.2f}")
