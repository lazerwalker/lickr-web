#!/usr/bin/python

from websocket import create_connection
import IPython

ws = create_connection("ws://lickr.herokuapp.com:80")

ws.send("machine")
print "Sent"
print "Receiving..."
while True:
    result =  ws.recv()
    print "Received '%s'" % result
ws.close()
