# -*- coding: utf-8 -*-
"""############################################################################
###
### Biomechanical Pandas Data Handling
### This file is part of Biomechanical-Pandas
### This file was created by Dr Daniel Parker on 23/12/18 
###    Twitter: @DrDanParker     GitHub:https://github.com/DrDanParker 
###     
### Copyright (C) 2018 University of Salford - All Rights Reserved
### You may use, distribute and modify this code under the terms of MIT Licence
### See LICENSE or go to https://tldrlegal.com/license/mit-license for full licence details
###
### Based on/Learnt from the following:
###     General panda docs and online tutorials
###     Learning the Pandas Library - Matt Harrison 2016 
###
############################################################################"""

import os
import pandas as pd

class BiomechData:
    
    # global bld_flist
    
    def __init__(self, fpath):
        self.fpath = fpath
        # self.data = pd.read_csv(self.fname,index_col=0) 
        
          
    def openPD(self,fname):
        fdat = pd.read_csv(fname,sep='\t',skiprows=list(range(9)))
        return(fdat)
    
    
    def bld_flist(self,ftype='.asc'):
        ''' builds list of all files in directory+subs with given file type '''
        flist = [os.path.join(r,file) for r,d,f in os.walk(self.fpath) for file in f 
            if file.endswith(ftype)]
        return(flist)
        
                
    def grp_by_part(self,seperator='_',level=0):
        ''' builds nested list of all files base on naming convention using _ - 
            can also be used to group files based on subdirectory using / or \\'''
        
        filelist = self.bld_flist()
        
        pref = []
        used = set()
        for file in filelist:
            pref.append(file.split(seperator)[level])
        unique = [x for x in pref if x not in used and (used.add(x) or True)]
        groups = []    
        for i in range(0,len(unique)):
            grp = []
            for j in range(0,len(pref)):
                if pref[j] == unique[i]:
                    grp.append(filelist[j])
            groups.append(grp)
        return(groups)
    
    
    def join_file(self,files,pad=100):
        ''' builds one dataframe from multiple file with the same data format '''
        fname = os.path.splitext(os.path.basename(files[0]))[0]
        dat =[]
        ind = range(pad)
        col = self.openPD(files[0]).columns
        if len(files) > 1: 
            for file in files:
                dat.append(self.openPD(file))
                pad_ = pd.DataFrame(index=ind,columns=col)
                pad_ = pad_.fillna(0)
                dat.append(pad_)
            odat = pd.concat(dat,axis=0)
        else:
            odat = self.openPD(files[0])    
        return odat,fname


################################################################################
###     Run Script
################################################################################
if __name__ == "__main__":
    mydir = 'C:/Temp/Test/' # either move to working directory or update to location
    d = BiomechData(mydir)
    data = d.join_file(files=d.bld_flist())
    print(data)
    
    # flist = d.bld_flist()

