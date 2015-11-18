# Lickr-web


## To set up a local copy

1. Clone this repo

2. `npm install`


## To run your local copy

`foreman start`

You should have a copy of the webapp running at http://localhost:5000.


## To connect

Start a new websocket connection to the appropriate URL. If you're a web client, send the string "web". If you're the Python machine, send the string "machine".

If you are a client, you can send coordinates by sending a string of the format "x, y,z" (e.g. "30,40,1" or "1.5,2.8,0.5"). That exact string will be passed along to the active machine, if any.

