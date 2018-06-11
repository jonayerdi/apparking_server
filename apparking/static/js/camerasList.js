
var $parkings;

function appendCamera(item, index) {
    $parkings.append("<li><a href=/cameras/"+item["pk"]+">"+item["number"]+"</a></li>")
}

function updateCameras() {
    $.ajax({
		url: '/api/cameras/',
        method : 'GET',
		success: function(data) {
			data["cameras"].forEach(appendCamera);
		},
		failure: function(data) { 
			console.warn("Failed request to /api/cameras/");
		}
	}); 
}

$(document).ready(function() {
    $parkings = $('#cameras');
    updateCameras();
});
