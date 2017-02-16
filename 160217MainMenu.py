#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 23:02:57 2017

@author: hanna-stinasonts
"""

'''

INTRODUCTION

Welcome to Hanna-Stina's dissertation Python baby.
You are currently in the 'cooking pot' of my code thing, meaning this is the place
where you want to define all your initial parameters, click run and let it work its
magic.


You will also need:

a) loading.py in order to be calculate all the loading conditions
(unless you are being adventurous and importing them with pandas from excel yourself)

b) struct_func.py aka structural engineering functions to be able to calculate all
the stresses and stuff


General point:

a) Dimensions - you set the maximum space limits, the real optimum structure might 
not actually need that much space so it's worth playing around with numbers


b) Material Limits - You can pick whichever but I have generally designed 
for steel beams meaning you'll probably be in the range of 275-355 N/mm2


c) Iteration paramters - aka the fun bit. 


Flange (f) - So for constructability reasons I have
incorporated a top flange bit, which means that no matter how the most efficient
profile might look like, the top of the section will never be removed.
you'll need a flat top to actually be able to build stuff on and it needs to be 
of acceptable thickness, so just 1mm will not do. 

Cuts - How many pieces do you want to divide your beam up to, the more the better 
and more accurate to extrapolate the sections to a whole beam.
This should be an even number if you want to have a cut through the middle (aka 
probably the most stressed region of your beam).
NB: the name 'cuts' is misleading i know but i can't be arsed to change it atm

Steps - Defines the step size of iteration. So if set to 1% or 0.01 in, then the
program will get rid of all elements that are stressed by less than  maxstress*0.01, with
the next round of iteration being maxstress*0.02 and so on.
NB: The tricky bit- you might think you are being super clever and saving time
by putting a fairly big step size (even with 0.1), but oh no, then the program will
spit you an error saying "Ay/A can't divide by 0" because you have accidentally 
got rid of all the elements in your cross-section. I'm sure there is a more
intelligent way arounf this but i've left things just at 0.01 for now. 

d) Loading - all pretty straighforwad but bear in mind to add already factored loading.

'''

#Python priginal functions
import numpy as np 
np.set_printoptions(precision = 1)   # Sets the rounding percision to 0.1

#Functions I've written myself for the purpose of the dissertation study
from struct_func import initial, iteration
from loading import loading 



###############################################################
######---THESE PARAMETERS NEED TO BE INPUT BY USER ---#########
###############################################################

# a) DIMENTIONS
# smallest iteration level is for a 1mm2 box


L = 100     #beam length in mm
b = 10      #how wide in mm
h = 10      #how tall in mm

# b) MATERIAL LIMITS

maxstress = 275 # Material stress limit in N/mm2

# c) ITEARATION PARAMETERS

f = 5         # Top flange thickness in mm
cuts = 4      # Number of sections the beam is cut up to, therefore always with cuts+1 points analysed 
step = 0.01   # Defines step size in itearation, the smaller the more accurate
              # NB! If the step is too big the program will want to
              # get rid of most elemenets in first round as the stresses
              # haven't had a change to redistribute- hence keep small enough

# d) LOADING

#In the vertical direction (major axis), where positive loading acts downwards
w1=0.1 #UDL loading in kN/m
P1=0.5 #Point Load value in kN
x1= 50 #Point load location from left end of beam in mm

#In the horizontal out of plane (minor axis), where positive loading acts ?????
w2=0 #UDL loading in kN/m
P2=0 #Point Load value in kN
x2=0 #Point load location from left end of beam in mm

#axial loading
P=0.1 #in kN



###############################################################
######---             CALCULATIONS                 ---#########
###############################################################


'''
'loading' is a function that calculates all the loading conditions along the beam
at cuts+1 locations. The results have been summarised in the matrix r where each column
represents a cut, with a total of 4 rows that contain in each row:
    1. The first row lists the location of the cut aka the x coordinate along the beam
    2. The next row has the shear force acting at that point
    3. Major bending moment
    4. Minor bending moment
'''

r= loading(L, cuts, w1, P1, x1, w2, P2, x2)
print (r)

'''

Now, knowing the loading conditions at each point, we go through a loop
along the length of the beam and iterate the perfect cross-section for 
each location.

'''
              

j=0
while (j<=cuts):
    
    #Geometrical locationon along the x axis in mm
    x= r[0,j] 
    # The shear force at that point
    S= r[1,j]
    #The major bending moment
    Mx= r[2,j]
    #Minor bending moment
    My= r[3,j]
    
    print ("At location x=", x, " the principal stresses are ","\n")

    '''
    Here I have used the 'initial' function to calculate the stresses 
    in original section. This step is not really necessary as the next function
    redoes it, but it's nice to be able to visually compare the initial section
    to the final I guess
    '''
    
    principal1 = (initial (h,b, Mx,My,S,P,maxstress) )
    print ("Initial results ","\n", principal1,"\n")
    
    '''
    The 'iteration' function goes within a loop at the single locations and
    retrieves the optimised cross-section for that single location
    '''
    
    remember = iteration (h,b,f,Mx,My,S,P,maxstress,step)
    print ("After iteration ","\n", remember, "\n")
    
    j=j+1
    
