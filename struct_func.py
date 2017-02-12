#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:30:04 2017

@author: hanna-stinasonts
"""
import numpy as np 
import copy
np.set_printoptions(precision=1)  

def geometry(m, b, h): 
    "Return the geometrical properties of cross-section" 
    

    
    #LOCATION OF NEUTRAL AXIS
    
    A=0.0
    Ay=0.0
    i=0
    j=0
    
    while ( i<h ):
        while ( j<b ):
            if ( (m[i,j])!=0) :      #If 0, then empty and not counted
                  A=A+1
                  Ay = Ay + (i+ 0.5) #i+1 to account for centrid of element (element height 1)
            j= j + 1
        i=i+1
        j=0

    ybary= Ay/A


    # CALCULATING SECOND MOMENT OF AREA

    Iy=0
    i=0             #Again, i and j are elements to help counting
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (m[i,j])!=0) :             #IF WOULD BE 0 WOULD BE EMPTY BOX
                  Iy=Iy+(abs (i+0.5-ybary))**2        
            j= j + 1
        i=i+1
        j=0

    return A, ybary, Iy
    
# CALCULATE BENDING STRESS IN EACH ELEMENT - major axis


def moment(m, M, b, h, ybar, I): 
    "Return the moment matrix" 
    
    moment1 = copy.deepcopy (m)  #deepcopy because normal copy doesn't work proper
    i=0
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (moment1 [i,j])!=0) :             
                moment1 [i,j] = (M*(ybar-i-0.5))/I
            j= j + 1
        i=i+1
        j=0

    return moment1

# CALCULATING SHEAR STRESSES IN EACH ELEMENT - major axis

def shear(m, S, b, h, ybary, Iy): 
    "Return the shear stresses matrix" 
    
    shear1 = copy.deepcopy (m)
 #   aymatrix = copy.deepcopy (m)

    i=0
    j=0
    As = 0  # To calculate the area in shear
    t = 0   # To calculate the breatd of area in a slither
    Ay=0


    while ( i<h ):                  #Starts to read from top first row down 
        while ( j<b ):              # Starts to read elements from left in frist row
            if ( (shear1[i,j])!=0) :   
                t= t+1
                As= As+1 
                Ay = Ay + 1*(ybary-i-0.5)
  #              aymatrix[i,j]=(ybary-i-0.5)
                
            j=j+1
        j=0
            
        while ( j<b ):              # Starts to read elements from left in frist row
            
            if ( (shear1[i,j])!=0) :   
                shear1[i,j]=(S*(Ay)/(Iy*t))     #NB the ybar-i/2 is a roug simplification of centroid
            j=j+1
        i=i+1
        j=0
        t=0
#        print (aymatrix)
    
    shear1[0, :] = 0 #Turn all first row values to zero 
        
    return shear1
    
# PRINCIPAL STRESSES

def principal (m, b, h, momentx, momenty, shear1):
    "Return the principal stresses matrix" 
    
    principal1 = copy.deepcopy (m)

    i=0
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (principal1 [i,j])!=0) :             
                principal1 [i,j] = (momentx[i,j] + momenty[i,j])/2 + (( ((momentx[i,j] - momenty[i,j])/2)**2 + (shear1[i,j])**2 )**(0.5))
            j= j + 1
        i=i+1
        j=0
    
    return principal1 
    
def initial (h,b,Mx,My,S,P,maxstress): 
    "Return the geometrical properties of cross-section" 
    
    from struct_func import geometry, moment, shear, principal 
    
    import numpy as np 
    import copy
    np.set_printoptions(precision=1)   # Sets the rounding percision to 0.1
    
    #Creating the matrix of a solid hxb element filled for the time with all values 1

    m = np.ones((h, b), dtype=np.float  )  #np.float isntead of int in order to get decimals
    mx= copy.deepcopy (m.transpose())      #same matrix turned around to work with x axis

    
    ##################################
    ####---1stTERATION SCRIPT------###
    ##################################

    #MAJOR AXIS GEOMETRY

    Y= (geometry(m,b,h))

    A =Y[0]
    ybary = Y[1]
    Iy = Y[2]

    #MINOR AXIS GEOMETRY

    Y= (geometry(mx,h,b))

    ybarx = Y[1]
    Ix = Y[2]

    # CALCULATE BENDING AND SHEAR IN EACH ELEMENT

    momentx= (moment(m,Mx,b,h,ybary,Iy))

    momenty= (moment (mx,My,h,b,ybarx,Ix))  #takes the turned around matrix to local axis
    momenty= copy.deepcopy (momenty.transpose()) # turns it back to aling global for summing purposes

    shear1 = (shear(m,S, b, h,ybary,Iy))
    axial1=P/A
    
    if (axial1 > maxstress):
        print("The maxstress is ", maxstress, " but the axial stress is ", axial1)
        print("Section is overstressed, choose different input", "\n")

    principal1 = (principal(m, b, h, momentx, momenty, shear1))
    
    return principal1
    
    
def iteration (h,b,Mx,My,S,P,maxstress,step): 
    "Return the first iterataion of the cross-section" 
    
    from struct_func import geometry, moment, shear, principal, initial 
    
    principal1 = (initial (h,b,Mx,My,S,P,maxstress) )
    
    # First Check if the elemenent is not already overstressed
    #checking for both princial and axial stresses

    if ( ((abs(principal1))>(maxstress)).any() ):
        print ("The max principal stress is more than allowed")
        print("Section is overstressed, choose different input", "\n")
    
    
  
    ##################################
    ###---1stITERATION SCRIPT------###
    ##################################

    else: 

        #print ("2. RUNNING ITERATION LOOP", "\n")
    
        kord=1 #Remembers the number of the iteration
    
        # First you check if the axial and principal stresses are within limits
        # Loop converges as it steps out of the limits

        absprincipal1= abs(principal1)  # You take abs as you have both +&- stresses
    
        # the while condition means that it checks the maximum absolute value of 
        # all non-zero elements to the max stress limit
    
        while ((np.max(absprincipal1[np.nonzero(absprincipal1)]))<maxstress):

            #This makes everything that is understressed value to nought
            # taking into account the step size and number of itearation 
        
            principal1[absprincipal1 < maxstress*step*kord] = 0

            # Then you remember the new matrix with removed material
            # and work with that instead
            m = copy.deepcopy(principal1) 
            mx= copy.deepcopy (m.transpose())

            #MAJOR AXIS GEOMETRY

            Y= (geometry(m,b,h))

            A =Y[0]
            ybary = Y[1]
            Iy = Y[2]
    
            #MINOR AXIS GEOMETRY

            Y= (geometry(mx,h,b))

            ybarx = Y[1]
            Ix = Y[2]
    
            # CALCULATE BENDING STRESS IN EACH ELEMENT
            momentx= (moment(m,Mx,b,h,ybary,Iy))

            momenty= (moment (mx,My,h,b,ybarx,Ix))
            momenty= copy.deepcopy (momenty.transpose())

            shear1 = (shear(m,S, b, h,ybary,Iy))
        
            principal1 = (principal(m, b, h, momentx, momenty, shear1))
        
            axial1=round(P/A,1)
        
            kord=kord+1
        
            absprincipal1= abs(principal1)  
        
            #REMEMBERING THE CORRECT VALUES
            # No values in principal matrix are greater than maxstress
            # AND axial stress is smaller than maxstress
    
            if ((np.max(absprincipal1[np.nonzero(absprincipal1)]))<maxstress) and (axial1<maxstress):
            
                remember= copy.deepcopy (principal1)
                #rememberkord= kord
            
        #print ("Results of ", rememberkord ,"nd iteration loop")

        #print (remember)
    
    return remember
