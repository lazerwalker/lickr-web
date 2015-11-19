  window.addEventListener('load', function() {

  	var canvas = document.getElementById("myCanvas");
    var height = self.innerHeight;
    var width = self.innerWidth;
    var size = Math.min (height, width)*0.95;
    canvas.height=size;
    canvas.width=size;

    var context = canvas.getContext('2d');
	context.lineWidth=8;

    // Touch events
    canvas.addEventListener('touchstart', function(e){
    	coords = getMousePos(canvas, e.touches[0].pageX, e.touches[0].pageY);
    	Server.send(coords.x, coords.y, 1);

    	context.beginPath();
        context.moveTo(coords.x, coords.y);
    }, false);

    canvas.addEventListener('touchmove', function(e){
    	coords = getMousePos(canvas, e.touches[0].pageX, e.touches[0].pageY);
    	Server.send(coords.x, coords.y, 1);

    	context.lineTo(coords.x, coords.y);
       	context.stroke();
    }, false);    

    canvas.addEventListener('touchend', function(e){
    	coords = getMousePos(canvas, e.touches[0].pageX, e.touches[0].pageY);
    	Server.send(coords.x, coords.y, 0);
    }, false);


    // Mouse events
    // (Just for demonstrative purposes)
    var mouseDown = false;

    canvas.addEventListener('mousedown', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY);
    	Server.send(coords.x, coords.y, 1);
    	mouseDown = true;

    	context.beginPath();
        context.moveTo(coords.x, coords.y);
    }, false);

    canvas.addEventListener('mousemove', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY);
    	var z = (mouseDown ? 1 : 0);
    	Server.send(coords.x, coords.y, z);

    	if (mouseDown) {
       	 context.lineTo(coords.x, coords.y);
       	 context.stroke();
      	}
    }, false);    

    canvas.addEventListener('mouseup', function(e){
    	coords = getMousePos(canvas, e.pageX, e.pageY);
    	Server.send(coords.x, coords.y, 0);
    	mouseDown = false;
    }, false);

}, false);

function getMousePos(canvas, evX, evY) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evX - rect.left,
      y: evY - rect.top
  };
}
