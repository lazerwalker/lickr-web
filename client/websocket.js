;(function() {

var server = location.origin.replace(/^http/, 'ws')
var socket = new WebSocket(server);

var isOpen = false;
var buffer = [];

socket.onopen = function() {
  socket.send("web");
  console.log("Opened");
  isOpen = true;
  if (buffer.length > 0) {
    buffer.forEach(function(msg) {
      socket.send(msg)
    });
    buffer = [];
  }
};

window.Server = {
  send: function(x, y, z) {
    var msg = [x,y,z].join(",");
    console.log("Sending", msg);
    if(isOpen) {
      socket.send(msg);
    } else {
      buffer.push(msg);
    }
  }
};

})();