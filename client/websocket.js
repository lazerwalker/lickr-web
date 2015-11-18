;(function() {

var server = location.origin.replace(/^http/, 'ws')
var socket = new WebSocket(server);
socket.onopen = function() {
  socket.send("web");
};

window.Server = {
  send: function(x, y, z) {
    socket.send([x,y,z].join(","));
  }
};

})();