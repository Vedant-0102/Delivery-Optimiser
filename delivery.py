import itertools

class DeliveryGraph:
    def __init__(self):
        self.locations = []
        self.distances = {}
        self.graph = {}

    def add_location(self, location):
        self.locations.append(location)
        self.graph[location] = {}

    def add_distance(self, from_location, to_location, distance):
        self.graph[from_location][to_location] = distance
        self.graph[to_location][from_location] = distance  # Bidirectional paths

def calculate_route_distance(route, graph):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += graph.graph[route[i]][route[i + 1]]
    return total_distance

def find_best_route(graph, start_location):
    locations = graph.locations.copy()  # Copy to avoid modifying the original list
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
