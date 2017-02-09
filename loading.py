def loading(L, cuts, w, P, x): 
    "Return the geometrical and loading properties in form of L, cuts, w, P, x where x is distance from left to pointload" 

    P=P*1000 #Conversion to N
    points= cuts+1
    r = np.ones((3, points), dtype=np.float  )

    #Therefore the points considered will be from beginning to end with intermediates
    #Location of points added to first row
    
    j=0
    while (j<=cuts):
    
        #geometrical locationon x axis
        r[0,j]=j*L/cuts 

        #Caluclating the Shear at the locations
        if r[0,j]<x: 
            r[1,j]= -(L-r[0,j])*P/L -(w*L/2-w*r[0,j])
        elif r[0,j]==x:
            r[1,j]=(w*L/2-w*r[0,j])
        else:
            r[1,j]= (r[0,j])*P/L -(w*L/2-w*r[0,j])
    
            #Calculatinf moments
        r[2,j]= (P*r[0,j]*(L-r[0,j])/L)+(w*r[0,j]*r[0,j]/2-w*L*r[0,j]/2)
    
        j=j+1
    
    return (r)
