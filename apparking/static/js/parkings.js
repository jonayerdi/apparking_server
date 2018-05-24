
var $parkingName;
var $parkingSpots;

function updateParkingName(name) {
    $parkingName.text(name);
}

function appendParkingSpot(spot) {
    state = spot["state"];
    $parkingSpots.append("<li id=spot\""+spot["number"]+"\"><ul><li>Number: "+spot["number"]
    +"</li><li>Status: <ul><li>State: "+state["state"]+"</li><li>Timestamp: "+state["timestamp"]+"</li></ul></li></ul></li>")
}

function requestParkingSpot(spotId) {
    $.ajax({
		url: '/api/parkings/?spot=' + spotId,
        method : 'GET',
		success: function(data) {
			appendParkingSpot(data);
		},
		failure: function(data) { 
			console.warn("Failed parking spot request to /api/parkings/");
		}
	}); 
}

function updateParkingSpots(spots) {
    $parkingSpots.empty();
    spots.forEach(requestParkingSpot);
}

function updateParking() {
    $.ajax({
		url: '/api/parkings/?id=' + parkingId,
        method : 'GET',
		success: function(data) {
			updateParkingName(data["name"]);
            updateParkingSpots(data["parking_spots"]);
		},
		failure: function(data) { 
			console.warn("Failed parking request to /api/parkings/");
		}
	}); 
}

$(document).ready(function() {
    $parkingName = $('#parkingName');
    $parkingSpots = $('#parkingSpots');
    updateParking();
});
