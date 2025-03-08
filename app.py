from flask import Flask, render_template, request, jsonify
from delivery import DeliveryGraph, find_best_route

app = Flask(__name__)

# Initialize an empty graph
graph = DeliveryGraph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    location = data.get('location')
    
    if location:
        graph.add_location(location)
        return jsonify({"message": f"Location {location} added."})
    return jsonify({"error": "Invalid location"}), 400

@app.route('/add_distance', methods=['POST'])
def add_distance():
    data = request.json
    from_location = data.get('from_location')
    to_location = data.get('to_location')
    distance = data.get('distance')

    if from_location and to_location and distance is not None:
        graph.add_distance(from_location, to_location, distance)
        return jsonify({"message": f"Distance added between {from_location} and {to_location}."})
    return jsonify({"error": "Invalid input"}), 400

@app.route('/calculate_best_route', methods=['POST'])
def calculate_best_route():
    data = request.json
    start_location = data.get('start_location')

    if start_location in graph.locations:
        best_route, min_distance = find_best_route(graph, start_location)
        return jsonify({"best_route": best_route, "total_distance": min_distance})
    return jsonify({"error": "Invalid starting location"}), 400

if __name__ == '__main__':
    app.run(debug=True)
