  window.addEventListener('load', function() {

  	var canvas = document.getElementById("myCanvas");
    var height = self.innerHeight;
    var width = self.innerWidth;
    var size = Math.min (height, width)*0.99;
    canvas.height=size;
    canvas.width=size;

    var context = canvas.getContext('2d');
    context.lineWidth=10;
    context.strokeStyle = "#FF1493";

    var prevX = 0;
    var prevY = 0;

    function sendPoint( x, y, z) {
        if (!isNaN(x) && !isNaN(y)) {
            Server.send(x, y, z);
            prevX = x;
            prevY = y;
        }
    }

    // Touch events

    canvas.addEventListener('touchstart', function(e){
    	coords = getMousePos(canvas, e.touches[0].pageX, e.touches[0].pageY, size);
    	sendPoint(coords.sendX, coords.sendY, 1);

    	context.beginPath();
        context.moveTo(coords.drawX, coords.drawY);
    }, false);

    canvas.addEventListener('touchmove', function(e){
    	coords = getMousePos(canvas, e.touches[0].pageX, e.touches[0].pageY, size);
    	sendPoint(coords.sendX, coords.sendY, 1);

    	context.lineTo(coords.drawX, coords.drawY);
        context.stroke();

        e.preventDefault();
    }, false);    

    canvas.addEventListener('touchend', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY, size);
    	sendPoint(prevX, prevY, 0);
    }, false);


    // Mouse events
    // (Just for demonstrative purposes)
    var mouseDown = false;

    canvas.addEventListener('mousedown', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY, size);
    	sendPoint(coords.sendX, coords.sendY, 1);
    	mouseDown = true;

    	context.beginPath();
        context.moveTo(coords.drawX, coords.drawY);
    }, false);

    canvas.addEventListener('mousemove', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY, size);
    	var z = (mouseDown ? 1 : 0);
    	sendPoint(coords.sendX, coords.sendY, z);

    	if (mouseDown) {
           context.lineTo(coords.drawX, coords.drawY);
           context.stroke();
       }
   }, false);    

    canvas.addEventListener('mouseup', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY, size);
    	sendPoint(coords.sendX, coords.sendY, 0);
    	mouseDown = false;
    }, false);

}, false);

  function getMousePos(canvas, evX, evY, size) {
    var rect = canvas.getBoundingClientRect();
    var drawX = evX - rect.left;
    var drawY = evY - rect.top;
    var sendNaN = drawX < 0 || drawX > size || drawY < 0 || drawY > size;
    var sendX = sendNaN? NaN : Math.round(drawX-(size/2));
    var sendY = sendNaN? NaN : Math.round(drawY-(size/2));
    return {
      drawX,
      drawY,
      sendX,
      sendY
  };
}
