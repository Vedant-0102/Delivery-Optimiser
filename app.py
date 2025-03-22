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
    try:
        data = request.json
        location = data.get('location')
        
        if not location:
            return jsonify({"error": "Location name cannot be empty"}), 400
            
        if location in graph.locations:
            return jsonify({"error": f"Location '{location}' already exists"}), 400
            
        graph.add_location(location)
        return jsonify({"message": f"Location '{location}' added successfully"})
    except Exception as e:
        app.logger.error(f"Error adding location: {str(e)}")
        return jsonify({"error": "Server error occurred"}), 500

@app.route('/add_distance', methods=['POST'])
def add_distance():
    try:
        data = request.json
        from_location = data.get('from_location')
        to_location = data.get('to_location')
        distance = data.get('distance')

        if not from_location or not to_location:
            return jsonify({"error": "Both locations must be specified"}), 400
            
        if from_location not in graph.locations:
            return jsonify({"error": f"Location '{from_location}' does not exist"}), 400
            
        if to_location not in graph.locations:
            return jsonify({"error": f"Location '{to_location}' does not exist"}), 400
            
        if distance is None or not isinstance(distance, (int, float)) or distance <= 0:
            return jsonify({"error": "Distance must be a positive number"}), 400

        graph.add_distance(from_location, to_location, distance)
        return jsonify({"message": f"Distance added between '{from_location}' and '{to_location}'"})
    except Exception as e:
        app.logger.error(f"Error adding distance: {str(e)}")
        return jsonify({"error": "Server error occurred"}), 500

@app.route('/calculate_best_route', methods=['POST'])
def calculate_best_route():
    try:
        data = request.json
        start_location = data.get('start_location')

        if not start_location:
            return jsonify({"error": "Start location cannot be empty"}), 400
            
        if start_location not in graph.locations:
            return jsonify({"error": f"Location '{start_location}' does not exist"}), 400
            
        if len(graph.locations) < 2:
            return jsonify({"error": "Need at least two locations to calculate a route"}), 400

        # Check if we have distances for all locations
        for loc in graph.locations:
            if loc != start_location and (loc not in graph.graph[start_location] or not graph.graph[start_location][loc]):
                return jsonify({"error": f"Missing distance between '{start_location}' and '{loc}'"}), 400

        best_route, min_distance = find_best_route(graph, start_location)
        return jsonify({"best_route": best_route, "total_distance": min_distance})
    except Exception as e:
        app.logger.error(f"Error calculating route: {str(e)}")
        return jsonify({"error": "Server error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
