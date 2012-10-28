// Generated by CoffeeScript 1.4.0
(function() {
  var canvas, ctx, onError, onSuccess, update, video, ws;

  onError = function(e) {
    return console.log("Rejected", e);
  };

  onSuccess = function(localMediaStream) {
    video.src = webkitURL.createObjectURL(localMediaStream);
    return setInterval(update, 250);
  };

  update = function() {
    ctx.drawImage(video, 0, 0, 320, 240);
    return canvas.toBlob(function(blob) {
      return ws.send(blob);
    }, 'image/jpeg');
  };

  video = document.querySelector('video');

  canvas = document.querySelector('canvas');

  ctx = canvas.getContext('2d');

  ws = new WebSocket("ws://" + location.host + "/socket");

  ws.onopen = function() {
    return console.log("Opened websocket");
  };

  ws.onmessage = function(e) {
    var target;
    e.data.contentType = "image/png";
    e.data.type = "image/png";
    console.log(e);
    target = document.getElementById('target');
    return target.src = window.webkitURL.createObjectURL(e.data);
  };

  navigator.webkitGetUserMedia({
    'video': true,
    'audio': false
  }, onSuccess, onError);

}).call(this);
