#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 23:02:57 2017

@author: hanna-stinasonts
"""


# import math
import numpy as np 
np.set_printoptions(precision=1)   # Sets the rounding percision to 0.1

from struct_func import initial, iteration
from loading import loading 

###############################################################
######---THERE PARAMETERS NEED TO BE INPUT BY USER ---#########
###############################################################

# GEOMETERY
# This means the smallerst iteration level is for a 1mm2 box

L = 100 #beam length in mm
b = 15 #how wide in mm
h = 15 #how tall in mm

#MATERIAL LIMITS
maxstress = 275 # Material stress limit in N/mm2

#ITEARATION PARAMETERS
cuts = 4 #Number of cuts taken along beam to be analysed 
step = 0.001   # Defines step size in itearation, the smaller the more accurate
              # NB! If the step is too big the program will want to
              # get rid of most elemenets in first round as the stresses
              # haven't had a change to redistribute- hence keep small enough

#LOADING
#In the vertical direction (major axis), where positive loading acts downwards
w1=0.1 #UDL loading in kN/m
P1=0.5 #Point Load value in kN
x1= 50 #Point load location from left end of beam in mm
#In the horizontal out of plane (major axis), where positive loading acts ??
w2=0 #UDL loading in kN/m
P2=0 #Point Load value in kN
x2=0 #Point load location from left end of beam in mm
#axial loading
P=0.1 #in kN



r= loading(L, cuts, w1, P1, x1, w2, P2, x2)

print (r)

# Now we separeate each slice and each loading condition 
# In order to be able to insert it into the iteration script 
              

j=0
while (j<=cuts):
    
    #geometrical locationon x axis
    x= r[0,j] 
    S= r[1,j]
    Mx= r[2,j]
    My= r[3,j]
    #Caluclating the Shear at the locations
    
    print ("At location x=", x, " the principal stresses are ","\n")
    
    principal1 = (initial (h,b,Mx,My,S,P,maxstress) )
    print ("Initial results ","\n", principal1,"\n")
    
    remember = iteration (h,b,Mx,My,S,P,maxstress,step)
    print ("After iteration ","\n", remember, "\n")
    
    j=j+1
    
    
