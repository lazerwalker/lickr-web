#!/usr/bin/python

from websocket import create_connection
from threading import Thread

class LickrListener:

    ws = None
    queue = []
    
    def create_connection(self, uri):
        self.ws = create_connection(uri)
        self.ws.send("machine")
   

    def run(self):

        while True:
            result = self.ws.recv()
            result = result.split(',')
            result = [ int(x) for x in result ]
            self.queue.append(result)
    
    def close(self):    
        self.ws.close()
        
    def pop_queue(self):
        if self.queue: #if the queue is not empty:
            return self.queue.pop(0) #TODO: very inefficient, maybe I should consider a different datastructure
        else:
            return None #nothing to return!
            
    def run_in_background(self):
        thread = Thread(target = ll.run)
        thread.start()

if __name__ == "__main__":
    #TODO: main method here
    ll = LickrListener()
    ll.create_connection("ws://lickr.herokuapp.com:80")
    ll.run_in_background()
    
    while True:
        popped = ll.pop_queue()
        if popped: #if it's not None
            print popped
