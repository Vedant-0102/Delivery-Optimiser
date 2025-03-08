async function addLocation() {
    const location = document.getElementById("locationInput").value;
    
    const response = await fetch('/add_location', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ location })
    });

    const result = await response.json();
    alert(result.message || result.error);
}

async function addDistance() {
    const from = document.getElementById("fromInput").value;
    const to = document.getElementById("toInput").value;
    const distance = document.getElementById("distanceInput").value;

    const response = await fetch('/add_distance', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ from_location: from, to_location: to, distance: parseInt(distance) })
    });

    const result = await response.json();
    alert(result.message || result.error);
}

async function calculateBestRoute() {
    const start = document.getElementById("startInput").value;

    const response = await fetch('/calculate_best_route', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ start_location: start })
    });

    const result = await response.json();
    if (result.best_route) {
        document.getElementById("routeResult").innerText = `Best Route: ${result.best_route.join(" -> ")}\nTotal Distance: ${result.total_distance}`;
    } else {
        alert(result.error);
    }
}