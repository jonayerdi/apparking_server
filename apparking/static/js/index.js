
var $parkings;

function appendParking(item, index) {
    $parkings.append("<li><a href=/parkings/"+item["key"]+">"+item["name"]+"</a></li>")
}

function updateParkings() {
    $.ajax({
		url: '/api/parkings/?names=1',
        method : 'GET',
		success: function(data) {
			data["parkings"].forEach(appendParking);
		},
		failure: function(data) { 
			console.warn("Failed request to /api/parkings/");
		}
	}); 
}

$(document).ready(function() {
    $parkings = $('#parkings');
    updateParkings();
});
