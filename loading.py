#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 20:56:17 2017

@author: hanna-stinasonts
"""

'''
I'm making a matrix to hold all my results
First row will have locatations along x axis in mm
Second row will have shears
Third row will be bending results in major axis
Forth row will have minor bending 
the length will correspend to each location and each value at location
'''

import numpy as np 
np.set_printoptions(precision=1)

def loading(L, cuts, w1, P1, x1, w2, P2, x2): 
    "Return the geometrical and loading properties in form of L, cuts, w1, P1, x1, w2, P2, x2 where x is distance from left to pointload" 

    P1=P1*1000 #Conversion to N
    P2=P2*1000 #Conversion to N
    points= cuts+1
    r = np.ones((4, points), dtype=np.float  )

    #Therefore the points considered will be from beginning to end with intermediates
    #Location of points added to first row
    
    j=0
    while (j<=cuts):
    
        #geometrical locationon x axis
        r[0,j]=j*L/cuts 
        #Caluclating the Shear at the locations
        if r[0,j]<x1: 
            r[1,j]= -(L-x1)*P1/L -(w1*L/2-w1*r[0,j])
            r[2,j]= (P1*(L-x1)/L*r[0,j])-(w1*r[0,j]*r[0,j]/2-w1*L*r[0,j]/2)
            r[3,j]= (P2*(L-x2)/L*r[0,j])-(w2*r[0,j]*r[0,j]/2-w2*L*r[0,j]/2)
        
        elif r[0,j]==x1:
            r[1,j]=(w1*L/2-w1*r[0,j])
            r[2,j]= (P1*(L-x1)/L*r[0,j])-(w1*r[0,j]*r[0,j]/2-w1*L*r[0,j]/2)
            r[3,j]= (P2*(L-x2)/L*r[0,j])-(w2*r[0,j]*r[0,j]/2-w2*L*r[0,j]/2)
        
        else:
            r[1,j]= (x1)*P1/L -(w1*L/2-w1*r[0,j])
            r[2,j]= (P1*(x1)/L*(L-r[0,j]))-(w1*r[0,j]*r[0,j]/2-w1*L*r[0,j]/2)
            r[3,j]= (P2*(x2)/L*(L-r[0,j]))-(w2*r[0,j]*r[0,j]/2-w2*L*r[0,j]/2)
        
        j=j+1
    
    return (r)
