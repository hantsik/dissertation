#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:56:17 2017

@author: hanna-stinasonts
"""

'''

The aim of this function is to calculate all the relavent loading information
and store the results in a matrix where each column represents one cut with the
rows storing the corresponding: 

First row will have locatations along x axis in mm
Second row will have shear forces at those locations
Third row will be bending moment results in major axis
Forth row will have minor bending 

'''

import numpy as np 
np.set_printoptions(precision=1)

def loading(L, cuts, w1, P1, x1, w2, P2, x2): 
    "Return the geometrical and loading properties in form of L, cuts, w1, P1, x1, w2, P2, x2 where x is distance from left to pointload" 

    P1=P1*1000 #Conversion to N
    P2=P2*1000 #Conversion to N
    
    #If you divide beam up to 4 elements you analyse 5 point, therefore:
    points= cuts+1
    
    # Create an empty matrix to store your results 
    r = np.ones((4, points), dtype=np.float  )

    '''
    Therefore you start moving along the x axis and calculating all the corresponding loads,
    while storing them in the correct row and column.
    
    As i have both UDL and a point load acting I'm using superposition
    and general basic formulas. 
    
    '''
    
    #I only need to move along columns
    j = 0
    while (j <= cuts):
    
        #Geometrical location along x axis
        
        r[0,j] = j * L / cuts 

        #Loads acting in the major axis
        
        if r[0,j] < x1: #Where x1 is the application point of the pointload
            
            #Shear
            r[1,j] = -(L - x1) * P1/L - (w1*L/2 - w1*r[0,j])
            #Major bending
            r[2,j] = (P1*(L-x1)/L*r[0,j]) - (w1*r[0,j]*r[0,j]/2 - w1*L*r[0,j]/2)
        
        elif r[0,j] == x1:
            
            r[1,j] = (w1*L/2 - w1*r[0,j])
            r[2,j] = (P1*(L-x1)/L*r[0,j]) - (w1*r[0,j]*r[0,j]/2 - w1*L*r[0,j]/2)
        
        else:
            
            r[1,j] = (x1)*P1/L - (w1*L/2-w1*r[0,j])
            r[2,j] = (P1*(x1)/L*(L-r[0,j])) - (w1*r[0,j]*r[0,j]/2 - w1*L*r[0,j]/2)
        
        #Loads acting in the minor axis
        
        if r[0,j] < x2: 
            
            #Minor bending
            r[3,j] = (P2*(L-x2)/L*r[0,j]) - (w2*r[0,j]*r[0,j]/2 - w2*L*r[0,j]/2)
        
        elif r[0,j] == x2:
            
            r[3,j] = (P2*(L-x2)/L*r[0,j]) - (w2*r[0,j]*r[0,j]/2 - w2*L*r[0,j]/2)
        
        else:
            
            r[3,j] = (P2*(x2)/L*(L-r[0,j])) - (w2*r[0,j]*r[0,j]/2 - w2*L*r[0,j]/2)   
         
        j = j + 1
    
    return (r)
