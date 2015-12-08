#!/usr/bin/python

from websocket import create_connection
from threading import Thread
from numpy import sqrt
from delta_machine import *

class LickrListener:

    ws = None
    queue = []
    
    # length of arms
    L = 285 #mm

    # Delta Radius - distance from edge of end effector to point under center of carriage
    DR = 110 #mm

    # distance the head extends below the effector (Length of tongue)
    Hcz = 55
    
    jog_height = 20 #raise or lower 2 cm
    
    
    #pix2mm = 190./125.
    pix2mm = 1.0
    
    down = True
    
    
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
            if result is not None:
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
        
        Z = coords[2]
        
        
        Z = Z * self.jog_height #coords[2] is 1 or 0, so this is jog_height or 0


        if Z == 1 and self.down:
            pass
        elif Z < 1 and self.down:
            self.down = False #jog up
        elif Z == 1 and not self.down:
            self.down = True #jog down
        elif Z < 1 and not self.down:
            #return None
            pass
            
        

        
        
        #Now, convert
        X *= self.pix2mm
        Y *= self.pix2mm
        

        

        
        L = self.L
        DR = self.DR
        Hcz = self.Hcz

        # A is the rode on the Y axis, B is 120 degrees clockwise from A, C is 120 degrees clockwise from 
        # X, Y ,Z are the input poin recieved from the user touch on the screen
        Az = sqrt(pow(L, 2) - pow((X - 0), 2) - pow((Y - DR), 2)) + Z - Hcz
        Bz = sqrt(pow(L, 2) - pow((X - DR*sqrt(3)/2), 2) - pow((Y + DR/2),2)) + Z - Hcz
        Cz = sqrt(pow(L, 2) - pow((X + DR*sqrt(3)/2), 2) - pow((Y + DR/2),2)) + Z - Hcz
        
        Az -= (207.91633650269813)
        Bz -= (207.91633650269813)
        Cz -= (207.91633650269813)
        
        print [Az, Bz, Cz]
        
        return [Az, Bz, Cz]

if __name__ == "__main__":
    #TODO: main method here
    
    stages = virtualMachine(persistenceFile = "test.vmp")

	# You can load a new program onto the nodes if you are so inclined. This is currently set to 
	# the path to the 086-005 repository on Nadya's machine. 
	#stages.xyNode.loadProgram('../../../086-005/086-005a.hex')
	
	# This is a widget for setting the potentiometer to set the motor current limit on the nodes.
	# The A4982 has max 2A of current, running the widget will interactively help you set. 
	#stages.xyNode.setMotorCurrent(0.7)

	# This is for how fast the 
    stages.abcNode.setVelocityRequest(8)	
	
	# Some random moves to test with

    
    
    
	
	# Move!
    """
    for move in moves:
        stages.move(move, 0)
        status = stages.aAxisNode.spinStatusRequest()
		# This checks to see if the move is done.
        while status['stepsRemaining'] > 0:
            time.sleep(0.001)
            status = stages.aAxisNode.spinStatusRequest()  
    """  
    
    
    ll = LickrListener("ws://lickr.herokuapp.com:80")
    
    ll.run_in_background()
    
    while True:
        next = ll.pop_queue()

        if(next):

            # translation from queue format to array inverse kinematics
            coords = next
            stages.move(coords, 0)
            
            # TODO: Figure out what the ideal way to poll for finishd status is. 
            # In the xy_plotter example, the xAxisNode is the only one that is polled.
            # Maybe the way the gestalt network works is there is only one output node
            # for status checking?
            statusX = stages.aAxisNode.spinStatusRequest()
            statusY = stages.bAxisNode.spinStatusRequest()
            statusZ = stages.cAxisNode.spinStatusRequest()

            while(statusX['stepsRemaining'] > 0 or statusY['stepsRemaining'] > 0 or statusZ['stepsRemaining'] > 0):
                time.sleep(0.001)
                statusX = stages.aAxisNode.spinStatusRequest()   
                statusY = stages.bAxisNode.spinStatusRequest()
                statusZ = stages.cAxisNode.spinStatusRequest()
	
