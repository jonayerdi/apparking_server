
var $parkingName;
var $parkingSpots;
var ws;

function subscribeParking() {
    var ws_path = 'ws://' + window.location.host + "/ws/parking/";
    ws  = new ReconnectingWebSocket(ws_path);
    ws.onopen = function(e) {
        console.log('WebSocket is open.');
        ws.send(JSON.stringify({
            'type': 'ParkingSubscribe',
            'parkingId': parkingId
        }));
    };
    ws.onclose = function(e) {
        console.log('WebSocket is closed.');
    };
    ws.onmessage = function(e) {
        var spot = JSON.parse(e.data);
        console.debug(spot);
        updateParkingSpot(spot);
    };
}

function updateParkingSpot(spot)
{
    $spotState = $('#spotState'+spot["spotId"]);
    $spotTimestamp = $('#spotTimestamp'+spot["spotId"]);
    if($spotState != null && $spotTimestamp != null)
    {
        $spotState.text("State: "+spot["state"]);
        $spotTimestamp.text("Timestamp: "+spot["timestamp"]);
    }
}

function updateParkingName(name) {
    $parkingName.text(name);
}

function appendParkingSpot(spot) {
    state = spot["state"];
    $parkingSpots.append("<li><ul><li>Number: "+spot["number"]+"</li><li>Status: <ul><li id=spotState"+spot["number"]
    +">State: "+state["state"]+"</li><li id=spotTimestamp"+spot["number"]+">Timestamp: "+state["timestamp"]+"</li></ul></li></ul></li>")
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
    subscribeParking();
});
