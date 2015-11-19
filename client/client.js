  window.addEventListener('load', function() {

  	var canvas = document.getElementById("myCanvas");
    var height = self.innerHeight;
    var width = self.innerWidth;
    var size = Math.min (height, width)*0.95;
    canvas.height=size;
    canvas.width=size;

    var context = canvas.getContext('2d');
	context.lineWidth=5;

    // Touch events
    canvas.addEventListener('touchstart', function(e){
    	coords = canvas.relMouseCoords(e);
    	Server.send(coords.x, coords.y, 1);

    	context.beginPath();
        context.moveTo(coords.x, coords.y);
    }, false);

    canvas.addEventListener('touchmove', function(e){
    	coords = canvas.relMouseCoords(e);
    	Server.send(coords.x, coords.y, 1);

    	context.lineTo(coords.x, coords.y);
       	context.stroke();
    }, false);    

    canvas.addEventListener('touchend', function(e){
    	coords = canvas.relMouseCoords(e);
    	Server.send(coords.x, coords.y, 0);
    }, false);


    // Mouse events
    // (Just for demonstrative purposes)
    var mouseDown = false;

    canvas.addEventListener('mousedown', function(e){
    	coords = canvas.relMouseCoords(e);
    	Server.send(coords.x, coords.y, 1);
    	mouseDown = true;

    	context.beginPath();
        context.moveTo(coords.x, coords.y);
    }, false);

    canvas.addEventListener('mousemove', function(e){
    	coords = canvas.relMouseCoords(e);
    	var z = (mouseDown ? 1 : 0);
    	Server.send(coords.x, coords.y, z);

    	if (mouseDown) {
       	 context.lineTo(coords.x, coords.y);
       	 context.stroke();
      	}
    }, false);    

    canvas.addEventListener('mouseup', function(e){
    	coords = canvas.relMouseCoords(e);
    	Server.send(coords.x, coords.y, 0);
    	mouseDown = false;
    }, false);

}, false);

function relMouseCoords(event){
    var totalOffsetX = 0;
    var totalOffsetY = 0;
    var canvasX = 0;
    var canvasY = 0;
    var currentElement = this;

    do{
        totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
        totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
    }
    while(currentElement = currentElement.offsetParent)

    canvasX = event.pageX - totalOffsetX;
    canvasY = event.pageY - totalOffsetY;

    return {x:canvasX, y:canvasY}
}
HTMLCanvasElement.prototype.relMouseCoords = relMouseCoords;
