#!/usr/bin/python

from websocket import create_connection
from threading import Thread
from numpy import sqrt

class LickrListener:

    ws = None
    queue = []
    
    # length of arms
    L = 285 #mm

    # Delta Radius - distance from edge of end effector to point under center of carriage
    DR = 190 #mm

    # distance the head extends below the effector (Length of tongue)
    Hcz = 55
    
    jog_height = 20 #raise or lower 2 cm
    
    PR = 128
    
    pix2mm = 190/125
    
    
    def __init__(self):
        pass
    
    def __init__(self, uri):
        self.create_connection(uri)
    
    def create_connection(self, uri):
        self.ws = create_connection(uri)
        self.ws.send("machine")
   

    def run(self):

        while True:
            result = self.ws.recv()
            result = result.split(',')
            result = [ int(x) for x in result ]
            #convert it:
            result = self.translate_coordinates(result)
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
        
    def translate_coordinates(self, coords):
    #Translates the coordinates from [x, y, z] to [A, B, C]

        #First step: center them
        X = coords[0]
        Y = coords[1]
        Z = coords[2] * self.jog_height #coords[2] is 1 or 0, so this is jog_height or 0
        
        #Now, convert
        X *= self.pix2mm
        Y *= self.pix2mm
        
        print X
        print Y
        print Z
        

        
        L = self.L
        DR = self.DR
        Hcz = self.Hcz

        # A is the rode on the Y axis, B is 120 degrees clockwise from A, C is 120 degrees clockwise from 
        # X, Y ,Z are the input poin recieved from the user touch on the screen
        Az = sqrt(pow(L, 2) - pow((X - 0), 2) - pow((Y - DR), 2)) + Z + Hcz
        Bz = sqrt(pow(L, 2) - pow((X - DR*sqrt(3)/2), 2) - pow((Y + DR/2),2)) + Z + Hcz
        Cz = sqrt(pow(L, 2) - pow((X + DR*sqrt(3)/2), 2) - pow((Y + DR/2),2)) + Z + Hcz
        
        return [Az, Bz, Cz]

if __name__ == "__main__":
    #TODO: main method here
    ll = LickrListener("ws://lickr.herokuapp.com:80")
    ll.run_in_background()
    
    while True:
        popped = ll.pop_queue()
        if popped: #if it's not None
            print popped
