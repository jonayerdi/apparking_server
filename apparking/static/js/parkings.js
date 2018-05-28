
var $parkingName;
var $parkingSpots;
var ws;
var spotNumber2spotId = {};

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
    spotId = spotNumber2spotId[spot["spotId"]];
    $spotState = $('#spotState'+spotId);
    $spotTimestamp = $('#spotTimestamp'+spotId);
    if($spotState != null && $spotTimestamp != null)
    {
        $spotState.text("State: "+spot["state"]);
        $spotTimestamp.text("Timestamp: "+spot["timestamp"]);
    }
}

function updateParkingName(name) {
    $parkingName.text(name);
}

function appendParkingSpot(spotId) {
    $parkingSpots.append("<li><ul><li id=spotNumber"+spotId
    +">Number: Requesting...</li><li>Status: <ul><li id=spotState"+spotId
    +">State: Requesting...</li><li id=spotTimestamp"+spotId+">Timestamp: Requesting...</li></ul></li></ul></li>")
}

function requestParkingSpot(spotId) {
    $.ajax({
		url: '/api/parkings/?spot=' + spotId,
        method : 'GET',
		success: function(data) {
            $spotNumber = $("#spotNumber"+spotId);
            $spotState = $("#spotState"+spotId);
            $spotTimestamp = $("#spotTimestamp"+spotId);
			$spotNumber.text("Number: " + data["number"]);
            $spotState.text("State: " + data["state"]["state"]);
            $spotTimestamp.text("Timestamp: " + data["state"]["timestamp"]);
            spotNumber2spotId[data["number"]] = spotId;
		},
		failure: function(data) { 
			console.warn("Failed parking spot request to /api/parkings/");
		}
	}); 
}

function updateParkingSpots(spots) {
    $parkingSpots.empty();
    spots.forEach(appendParkingSpot);
    spots.forEach(requestParkingSpot);
    subscribeParking();
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
