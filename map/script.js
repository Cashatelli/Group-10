// Initialize the map
var map = L.map('map').setView([39.8283, -98.5795], 4); // Centered at (0, 0) with zoom level 2

// Add the OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Function to calculate distance between two points using Haversine formula
function haversine(lat1, lon1, lat2, lon2) {
    const R = 3958.8; // Radius of the Earth in miles
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = R * c; // Distance in miles
    const feet = distance * 5280; // Convert to feet
    return { miles: distance, feet: feet };
}

// Function to handle successful location retrieval
function onLocationFound(e) {
    var radius = e.accuracy / 2;

    // Set the view to the user's location
    map.setView(e.latlng, 10);

    rentalLocations.forEach(function (location) {
        var distances = haversine(e.latlng.lat, e.latlng.lng, location.lat, location.lng);
        L.marker([location.lat, location.lng])
            .addTo(map)
            .bindPopup(location.name + "<br>Distance: " + distances.miles.toFixed(2) + " miles (" + distances.feet.toFixed(2) + " feet)");
    });

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

    L.circle(e.latlng, radius).addTo(map);
}

// Function to handle location retrieval error
function onLocationError(e) {
    alert("Error: " + e.message);
}

// Set up event listeners for location found and error
map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

// Request the user's location
map.locate({ setView: true, maxZoom: 10 });

// Add rental locations
var rentalLocations = [
    { lat: 35.7796, lng: -78.6382, name: 'Raleigh, North Carolina' },
    { lat: 35.5951, lng: -77.3739, name: 'Greenville, North Carolina' },
    { lat: 35.2271, lng: -80.8431, name: 'Charlotte, North Carolina' },
    { lat: 40.7128, lng: -74.0060, name: 'New York City, New York' },
    { lat: 25.7617, lng: -80.1918, name: 'Miami, Florida' },
    { lat: 33.7490, lng: -84.3880, name: 'Atlanta, Georgia' },
    { lat: 32.7765, lng: -79.9311, name: 'Charleston, South Carolina' },
];


