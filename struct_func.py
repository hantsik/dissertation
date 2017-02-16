#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:30:04 2017

@author: hanna-stinasonts
"""

'''
INTRO

This is just a long list of functions that I have used in the code
The functions can be divided up to 

a) Basic - functions that use predefined paramters and built in functions.
These are all based on textbook structral engineering formulas.

b) Advanced - functions that use SOME predefined paramters but calculate 
most by using the user-written and then imported Basic functions. 

'''


# not really sure if these need to be here but just kindof left it like that
import numpy as np 
import copy
np.set_printoptions(precision=1)  #set working precision to .1


    ##################################
    ####---BASIC FUNCTIONS---------###
    ##################################
    

def geometry(m, b, h): 
    "Return the geometrical properties of cross-section, including the area, location of neutral axis, and second moment of area" 
    
    #LOCATION OF NEUTRAL AXIS
    
    A = 0.0     #Area
    Ay = 0.0    #First moment of area
    i = 0
    j = 0
    
    while ( i<h ):
        while ( j<b ):
            if ( (m[i,j]) != 0) :      #If 0, then considered as empty and not counted
                  A=A+1
                  Ay = Ay + (i+ 0.5) #i+0.5 to account for centrid of element (element height 1)
            j= j + 1
        i=i+1
        j=0

    ybary= Ay/A #Location of neutral axis


    # CALCULATING SECOND MOMENT OF AREA

    Iy=0 #Second moment of area
    i=0             #Again, i and j are elements to help counting
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (m[i,j])!=0) :             #As 0 would bean an elements with no area
                  Iy = Iy + ( abs(i+0.5-ybary) )**2        
            j= j + 1
        i=i+1
        j=0

    return A, ybary, Iy
    
# CALCULATE BENDING STRESS IN EACH ELEMENT - major axis


def moment(m, M, b, h, ybar, I): 
    "Return the moment matrix" 
    
    #Make a copy of the element matrix and substitue values with moment stresses
    moment1 = copy.deepcopy (m)  #deepcopy because normal copy doesn't work proper
    i=0
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (moment1 [i,j]) != 0) :             
                moment1 [i,j] = (M*(ybar-i-0.5))/I #Calculates bending stress in each element
            j= j + 1
        i=i+1
        j=0

    return moment1

# CALCULATING SHEAR STRESSES IN EACH ELEMENT - major axis

def shear(m, S, b, h, ybary, Iy): 
    "Return the shear stresses matrix" 
    
    shear1 = copy.deepcopy (m)

    i=0
    j=0
    As = 0  # To calculate the area in shear
    t = 0   # To calculate the breadth of a slither
    Ay=0

    '''
    The shear stress formula is a bit funny, 
    first you need to go through each row to know how many elements in slither
    are carrying the stress and what is the total area above slither.
    Then knowing this, you can go through the row again and applu the same
    shear stress value to all the elements, hence the double loop.
    
    '''
    
    
    while ( i<h ):                  #Starts to read from top first row down 
    
        #The loop where you count elements in and up to end of row
        while ( j<b ):              # Starts to read elements from left in frist row
            if ( (shear1[i,j])!=0) :   
                t= t+1
                As= As+1 
                Ay = Ay + 1*(ybary-i-0.5)
                
            j=j+1
        j=0
        
        #Loop where you assign values to elements in row
        while ( j<b ):              # Starts to read elements from left in frist row
            
            if ( (shear1[i,j])!=0) :   
                shear1[i,j]=(S*(Ay)/(Iy*t))     #NB the ybar-i/2 is a roug simplification of centroid
            j=j+1
        j=0
        
        i=i+1
        t=0
    
    '''
    Another slightly tricky bit here. 
    
    Because I have taken cuts through the bottom of the element row it means that 
    it will produce results where the top row as some shear in it with the bottom
    row being all elemenst 0. I'm going to fix the top row value to always be zero because
    that would be most correct in the theorical terms. 
    
    Although practically this doesn't make much difference to the results, but 
    I would prefer to keep top and bottom results symmetrical. 
    
    '''
    
    shear1[0, :] = 0 #Turn all first row values to zero 
        
    return shear1
    
# PRINCIPAL STRESSES

def principal (m, b, h, momentx, momenty, shear1):
    "Return the principal stresses matrix" 
    
    '''
    So here comes two more tricky parts

    Tricky nr 1

    I want to compare the MAX principal stress which could be both pos or neg
    Python always takes the pos value of a square root, therefore i need to try out
    total principal stress with both the pos or neg value of squareroot
    Hence the z with '+' and w with '-'
    Then i go on to compare the two values in abs terms, and assign the bigger 
    one to element.

    Tricky (and questionable) nr 2 - NEEDS TO BE REVISED/CONFIRMED

    Initially I had just abs(z) > abs(w), and not really thinking about what will
    happen if abs(z) = abs (w).
    Then I realised if abs(z) = abs (w) it means that (momentx[i,j] + momenty[i,j])/2 
    value must be 0, meaning the only force acting would be the shear force.

    I have used an arbitraru sign convention currently for the shear force so 
    not really sure what sign it should be but have left it as pos for now. 
                
    '''
    
    principal1 = copy.deepcopy (m)

    i=0
    j=0

    while ( i<h ):
        while ( j<b ):
            if ( (principal1 [i,j])!=0) :             
                
                # Tricky nr 1
                
                z = (momentx[i,j] + momenty[i,j])/2 + (( ((momentx[i,j] - momenty[i,j])/2)**2 + (shear1[i,j])**2 )**(0.5))
                w = (momentx[i,j] + momenty[i,j])/2 - (( ((momentx[i,j] - momenty[i,j])/2)**2 + (shear1[i,j])**2 )**(0.5))
                
                #Tricky (and questionable) nr 2 - NEEDS TO BE REVISED/CONFIRMED
                
                if (abs(z) >= abs(w)):  
                    principal1 [i,j]=z
                else:
                    principal1 [i,j]=w
                
            j= j + 1
        i=i+1
        j=0
    
    return principal1 
    
    
    
    
    
    ##################################
    ####---ADVANCED FUNCTIONS------###
    ##################################
  
    
def initial (h,b,Mx,My,S,P,maxstress): 
    "Return the geometrical properties of cross-section" 
    
    '''
    This function calculates the round 0 principal stresses, meaning in the 
    cross-section where no material has yet to be removed, utilising the above 
    written functions.
    
    '''
    from struct_func import geometry, moment, shear, principal 
    
    import numpy as np 
    import copy
    np.set_printoptions(precision=1)   # Sets the rounding percision to 0.1
    
    #Creating the matrix of a solid hxb element filled for the time with all values 1

    m = np.ones((h, b), dtype=np.float  )  #np.float isntead of int in order to get decimals
    mx= copy.deepcopy (m.transpose())      #same matrix turned around to work with minor axis

    #MAJOR AXIS GEOMETRY

    Y= (geometry(m,b,h))

    A =Y[0]
    ybary = Y[1]
    Iy = Y[2]

    #MINOR AXIS GEOMETRY

    Y= (geometry(mx,h,b)) #notice how you have to swap b and h here to work in minor 

    ybarx = Y[1]
    Ix = Y[2]

    # CALCULATE BENDING AND SHEAR IN EACH ELEMENT

    momentx= (moment(m,Mx,b,h,ybary,Iy))

    momenty= (moment (mx,My,h,b,ybarx,Ix))  #takes the turned around matrix to local axis
    momenty= copy.deepcopy (momenty.transpose()) # turns it back to aling global axes for summing purposes

    shear1 = (shear(m,S, b, h,ybary,Iy))
    axial1=P/A
    
    #This is a check to ensure that axial stresses within the stress limits
    
    if (axial1 > maxstress):
        print("The maxstress is ", maxstress, " but the axial stress is ", axial1)
        print("Section is overstressed, choose different input", "\n")

    principal1 = (principal(m, b, h, momentx, momenty, shear1))
    
    return principal1
    
    
    
    
def iteration (h,b,f, Mx,My,S,P,maxstress,step): 
    "Return the final iterataion of the cross-section" 
    
    from struct_func import geometry, moment, shear, principal, initial 
    
    # The function produces a set of initial principal stresses results
    
    principal1 = (initial (h,b,Mx,My,S,P,maxstress) )
    
    # Then it checks if the principal stresses are within limits

    if ( ((abs(principal1))>(maxstress)).any() ):
        print ("The max principal stress is more than allowed")
        print("Section is overstressed, choose different input", "\n")
    
    # If there is no error message, it proceeds to the iteration loop
    
    else: 
    
        kord=1 #Remembers the number of the iteration
   
        absprincipal1= abs(principal1)  # You take abs as you have both +&- stresses
    
        '''
        Here I have incoprorated a boundary condition for constructability purposes.
        No matter how small the stresses ight be, it will always keep a flat top flange.
        
        To do this, I have only allowed the loop the delete elements that are below
        the predefine flange thickness of f. 
        
        Therefore the iteration loop will stop if it has either reached the
        'perfect optimum' section (meaning that material stresses are as close to max
        as possible)
        OR
        If all elements below the flange have already been deleted. 
        
        To check the latter I have made a new matric which contains all the elements
        stresses below the flange. If all these are 0 the iteration loop will close.
        
        '''
        
        #Matrix of element stresses below the flange
        flange =  np.delete(principal1, np.s_[0:(f)], axis=0)
        
        '''
        The while conditon:
        
        Checks the maximum absolute value of all non-zero elements to be smaller than max stress limit
        And if all elements within flange matrix are not zero.
        If either case is true the loop will stop.
        
        '''
    
        while (((np.max(absprincipal1[np.nonzero(absprincipal1)]))<maxstress) & np.any(flange)):

            
            '''
            This loop makes everything that is understressed value to nought
            taking into account the step size and number of itearation.
            
            Starting from row f means that no elements within flange will be deleted. 
        
            '''
        
            i=f
            j=0

            while ( i<h ):
                
                print (i)
                while ( j<b ):
                    if ( absprincipal1[i,j] < maxstress*step*kord ): 
                        #print (absprincipal1[i,j] < maxstress*step*kord)
                        principal1 [i,j] = 0
                    j= j + 1
                i=i+1
                j=0
                
            #print ("after removing material new matrix is, ", "\n", principal1 )
                                
            # Then you remember the new matrix with removed material and work with that instead
            
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
    
            # CALCULATE STRESSes IN EACH ELEMENT
                        
            momentx= (moment (m,Mx,b,h,ybary,Iy))

            momenty= (moment (mx,My,h,b,ybarx,Ix))
            momenty= copy.deepcopy (momenty.transpose())

            shear1 = (shear(m,S, b, h,ybary,Iy))
            
            # COMBINES TO PRINCIPAL
            principal1 = (principal(m, b, h, momentx, momenty, shear1))
            
            # REPRODUCES THE NEW FLANGE MATRIC OF ELEMENTS BELOW IT
            flange =  np.delete(principal1, np.s_[0:(f)], axis=0)
            
            
            #print ("momentx ", momentx, "\n")
            #print ("momenty ", momenty, "\n")
            #print ("shear ", shear1 , "\n")
            
            #print ("having recalculated principal stresses for new shape ","\n", principal1)
        
            axial1 = round(P/A,1)
        
            kord = kord + 1
        
            absprincipal1= abs(principal1)  
        
            '''
            The iteration loop will stop if any stress value has gone above limit.
            Therefore we need to retrieve the results from before this happened, which is what
            the 'remember' bit below does.
            
            '''
            
            #REMEMBERING THE CORRECT VALUES
            
            # No values in principal matrix are greater than maxstress
            # AND axial stress is smaller than maxstress
    
            if ((np.max(absprincipal1[np.nonzero(absprincipal1)])) < maxstress) and (axial1 < maxstress):
            
                remember= copy.deepcopy (principal1)

    return remember
