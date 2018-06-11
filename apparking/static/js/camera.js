var $cameraImage;
var updateCameraImageIntervalID;

function updateCameraImage() {
    $cameraImage.attr("src","/cameras/image/" + cameraId);
}

$(document).ready(function() {
    $cameraImage = $('#cameraImage');
    updateCameraImageIntervalID = setInterval(function(){updateCameraImage()}, 3000);
});
