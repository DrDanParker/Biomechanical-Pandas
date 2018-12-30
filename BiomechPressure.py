###############################################################################
###
### BiomechPressure
### This file is part of GitHub Repository Biomechanical-Pandas
### This file was created by Dr Daniel Parker 
### includes a set of fuctions to process walking data from pedar 
###   
### Copyright (C) 2018 University of Salford - All Rights Reserved
### You may use, distribute and modify this code under the terms of MIT Licence
### See LICENSE file in Biomechanical-Pandas for full details
###
###############################################################################

import pandas as pd

class PedarData:
    """ Data handling for ascii output from Pedar Inshoe Pressure """ 
    
    def __init__(self,fname):
        self.fname = fname     # File to load
        
    def pedar_to_dframe(self):
        """ loads standard insole pair from pedar, skips headers """
        ### Setup DataFrame
        fdat = pd.read_csv(self.fname,sep='\t',skiprows=list(range(9)))
        heads = list(fdat.head(0))
        ###Split to Left and Right Insole Raw Data:        
        if len(heads) >= 199:
            Left = fdat.loc[:,heads[1]:heads[99]]
            Right = fdat.loc[:,heads[100]:heads[198]]
        else:
            print('ERROR: Sensor number too low') 
        ### Build DataFrame Map
        fmap = {"Left":Left,"Right":Right}
        return(fmap)
        
        
################################################################################
###     Run Script
################################################################################

if __name__ == "__main__":
    fname = '.\pressure_example.asc' # either move to working directory or update to location
    p = PedarData(fname)
    fmap = p.pedar_to_dframe()
    
    print(fmap)
