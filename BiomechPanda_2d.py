# -*- coding: utf-8 -*-
"""############################################################################
###
### Biomechanical Pandas 2D Time Series
### This file is part of Biomechanical-Pandas
### This file was created by Dr Daniel Parker on 14/12/18 
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


class Biomech2D:
    
    def __init__(self, fname):
        self.fname = fname
        self.data = pd.read_csv(self.fname,index_col=0) #import and set time as index
            #other file handling methods @ github.com/DrDanParker/Data-Handling

    def descriptive(self): # pandas does also have a builtin describe function.
        '''
        Builds a DataFrame with relevant descriptive statistics
        ''' 
        Descriptives = pd.DataFrame(columns=self.data.columns)
        Descriptives.loc['Count'] = self.data.count()
        Descriptives.loc['Mean'] = self.data.mean() 
        Descriptives.loc['SD'] = self.data.std()
        Descriptives.loc['Variance'] = self.data.var()
        Descriptives.loc['Sum'] = self.data.sum()
        Descriptives.loc['Min'] = self.data.min()
        Descriptives.loc['Max'] = self.data.max()
        Descriptives.loc['Range'] = Descriptives.loc['Max'] - Descriptives.loc['Min']
        Descriptives.loc['SEM'] = self.data.sem() # Standard Error of the Mean
        Descriptives.loc['Skewness'] = self.data.skew()
        Descriptives.loc['Kurtosis'] = self.data.kurtosis()
        return(Descriptives)
    
    def linear_calib(self,intercept,slope,inplace=True):
        '''
        Linear calibrations typically used to convert voltage output to scale
        '''
        if inplace==True:         #Replace original data
            return(slope*self.data+intercept)
        else:                     #Create new columns to retain original data
            for col in list(self.data.columns.values):
                self.data[col+'_calib'] = slope*self.data[col]+intercept
            return(self.data)
    
    
    def partwise_linear_calib(self,intercepts,slopes,breaks,inplace=True):
        '''
        Linear calibrations typically used to convert voltage output to scale
        '''
        def func(data,colname=''):
            for i,s,b in itertools.zip_longest(intercepts,slopes,breaks):
                    for col in list(data.columns.values):
                        if b != None:
                            data[col+colname] = data[col].apply(
                                        lambda x: (s*x)+i if x>=b else x)
                        else:
                            data[col+colname] = data[col].apply(
                                        lambda x: (s*x)+i if x<breaks[-1] else x)
            return(data)
        
        breaks.sort() # ensures breaks are in ascending order
        if inplace==True: #Replace original data
            self.data = func(self.data)
        else: #Create new columns to retain original data
            self.data = func(self.data,colname='_calib')
        return self.data



################################################################################
###     Run Script
################################################################################

import pandas as pd

fname = '.\example.csv' # either move to working directory or update to location
d = Biomech2D(fname)
print(d.data)
print(d.linear_calib(-6.151, -335.49,inplace=False))
