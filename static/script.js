async function addLocation() {
    const location = document.getElementById("locationInput").value.trim();
    
    if (!location) {
        alert("Please enter a location name");
        return;
    }
    
    try {
        const response = await fetch('/add_location', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ location })
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            document.getElementById("locationInput").value = "";
        } else {
            alert(result.error || "An error occurred");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server");
    }
}

async function addDistance() {
    const from = document.getElementById("fromInput").value.trim();
    const to = document.getElementById("toInput").value.trim();
    const distance = document.getElementById("distanceInput").value.trim();

    if (!from || !to || !distance) {
        alert("Please fill all fields (From, To, and Distance)");
        return;
    }
    
    if (isNaN(distance) || parseInt(distance) <= 0) {
        alert("Distance must be a positive number");
        return;
    }

    try {
        const response = await fetch('/add_distance', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                from_location: from, 
                to_location: to, 
                distance: parseInt(distance) 
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            document.getElementById("fromInput").value = "";
            document.getElementById("toInput").value = "";
            document.getElementById("distanceInput").value = "";
        } else {
            alert(result.error || "An error occurred");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server");
    }
}

async function calculateBestRoute() {
    const start = document.getElementById("startInput").value.trim();

    if (!start) {
        alert("Please enter a start location");
        return;
    }

    try {
        const response = await fetch('/calculate_best_route', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ start_location: start })
        });

        const result = await response.json();
        
        if (response.ok) {
            document.getElementById("routeResult").innerText = `Best Route: ${result.best_route.join(" -> ")}\nTotal Distance: ${result.total_distance}`;
        } else {
            alert(result.error || "An error occurred");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the server");
    }
}
