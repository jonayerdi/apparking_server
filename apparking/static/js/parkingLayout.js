
var parkingName;
var backgroundURL;
var spots;
var spotNumber2spotId = {};
var spotColors = {
    "Unknown": "gray",
    "Free": "green",
    "Freeing": "purple",
    "Taken": "red",
    "Taking": "yellow",
    "Reserved": "blue",
}

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
        updateParkingSpot(spotNumber2spotId[spot["spotId"]], spot["state"]);
    };
}

function updateParkingSpot(spotId, state)
{
    spots[spotId]["state"] = state;
    updateParkingSVG();
}

function updateParkingName(name) {
    $('#parkingName').text(name);
}

function requestParkingSpot(spotId) {
    $.ajax({
		url: '/api/parkings/?spot=' + spotId,
        method : 'GET',
		success: function(data) {
            spotNumber2spotId[data["number"]] = spotId;
            state = data["state"]["state"];
            if(state == "Free" && data["reservation"] != null)
            {
                state = "Reserved";
            }
            updateParkingSpot(spotId, state);
		},
		failure: function(data) { 
			console.warn("Failed parking spot request to /api/parkings/");
		}
	}); 
}

function updateParkingSVG() {
    svgElement = "<svg id='layoutSVG' height='600' width='800'><image height='600' width='800' xlink:href='"+backgroundURL+"'></image>";
    for (var key in spots) {
        if (spots.hasOwnProperty(key)) {
            x = spots[key]["x1"];
            y = spots[key]["y1"];
            w = spots[key]["x2"] - x;
            h = spots[key]["y2"] - y;
            color = spotColors[spots[key]["state"]];
            svgElement += "<rect x='"+x+"' y='"+y+"' width='"+w+"' height='"+h+"' style='fill:"+color+";fill-opacity:0.5;' />";
        }
    }
    svgElement += "</svg>";
    $('#layout').html(svgElement);
}

function updateLayoutInfo(layoutURL) {
    $.ajax({
        url: layoutURL,
        method : 'GET',
        success: function(data) {
            data["spots"].forEach(function(element){
                spots[element["id"]]["x1"] = element["x1"];
                spots[element["id"]]["x2"] = element["x2"];
                spots[element["id"]]["y1"] = element["y1"];
                spots[element["id"]]["y2"] = element["y2"];
            });
            updateParkingSVG();
            subscribeParking();
        },
        failure: function(data) { 
            console.warn("Failed parking request to " + layoutURL);
        }
	}); 
}

function updateParking() {
    $.ajax({
		url: '/api/parkings/?id=' + parkingId,
        method : 'GET',
		success: function(data) {
			parkingName = data["name"];
            backgroundURL = data["image"];
            spots = {};
            data["parking_spots"].forEach(function(element) {
                spots[element] = {
                    "x1": 0,
                    "x2": 0,
                    "y1": 0,
                    "y2": 0,
                    "state": "Unknown"
                };
                requestParkingSpot(element);
            });
            $('#parkingName').text(parkingName);
            updateLayoutInfo(data["layout"]);
		},
		failure: function(data) { 
			console.warn("Failed parking request to /api/parkings/");
		}
	}); 
}

$(document).ready(function() {
    updateParking();
});
