import math

# lenght of arms
L = 10

# Delta Radius - distance from edge of end effector to point under center of carriage
DR = 10

# distance the head extends below the effector (Lenght of toung)
Hcz = 5

# A is the rode on the Y axis, B is 120 degrees clockwise from A, C is 120 degrees clockwise from 
# X, Y ,Z are the input poin recieved from the user touch on the screen
Az = math.sqrt(L^2 - (X - 0)^2 - (Y - DR))^2) + Z + Hcz
Bz = math.sqrt(L^2 - (X - DR*math.sqrt(3)/2)^2 - (Y + DR/2)^2) + Z + Hcz
Cz = math.sqrt(L^2 - (X + DR*math.sqrt(3)/2)^2 - (Y + DR/2)^2) + Z + hcz