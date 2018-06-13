var $cameraImage;
var ws;

function subscribeCamera() {
    var ws_path = 'ws://' + window.location.host + "/ws/camera/";
    ws  = new ReconnectingWebSocket(ws_path);
    ws.onopen = function(e) {
        console.log('WebSocket is open.');
        ws.send(JSON.stringify({
            'type': 'CameraSubscribe',
            'cameraId': cameraId
        }));
    };
    ws.onclose = function(e) {
        console.log('WebSocket is closed.');
    };
    ws.onmessage = function(e) {
        var msg = JSON.parse(e.data);
        console.debug(msg);
        updateCameraImage();
    };
}

function updateCameraImage() {
    $cameraImage.attr("src","/cameras/image/" + cameraId);
}

$(document).ready(function() {
    $cameraImage = $('#cameraImage');
    updateCameraImage();
    subscribeCamera();
});
