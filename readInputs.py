# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 17:06:35 2020

@author: AntoniaPraetorius
"""

from Particulates import Particulates #import class to generate MP and SPM objects
import pandas as pd 
from pathlib import Path
import sys
import datetime



#function to read lake data
def lakeData(fileToOpen):
    try:
        compartments_prop = pd.read_csv(fileToOpen, comment='#')
    except IOError:
        print("File not accessible")
        sys.exit(1)  

    sanityCheckData(compartments_prop)          
    return compartments_prop   
                   
      
def sanityCheckData(dataFrame):
    #check if there is any negative value
    #check the dataframe type
    a=dataFrame.dtypes
    for i in range(len(a)):
    #include only the numerical fields
        if a[i]!="object": 
            #accepts only positive values
            if any(dataFrame[a.index[i]]<0):
                print("Error! Negative values in the column :" + a.index[i])
                sys.exit(1)  

#function to read microplastic data         
def microplasticData(fileToOpen):
    try:
        plastics_prop = pd.read_csv(fileToOpen, comment='#')
    except IOError:
        print("File not accessible")
        sys.exit(1)
    
    sanityCheckData(plastics_prop)      #need to make this specific to process info    
    return plastics_prop      

#function to read process info data         
def processData(fileToOpen):
    try:
        process_prop = pd.read_csv(fileToOpen, comment='#')
    except IOError:
        print("File not accessible")
        sys.exit(1)
    
    sanityCheckData(process_prop)          
    return process_prop      

#function to read daily emission data         
def processDailyInputData(fileToOpen):
    try:
        process_prop = pd.read_csv(fileToOpen, comment='#')
    except IOError:
        print("File not accessible")
        sys.exit(1)
    
    sanityCheckData(process_prop)          
    return process_prop      



def dateRangeGenerator(dayFirst,dayLast,mode):
    try:
        if mode=="Monthly":
            #dayFirst must be < dayLast
            if dayFirst > dayLast :
               print("Wrong dates order")
               sys.exit(1)
               
            if dayFirst.month == dayLast.month and dayFirst.year == dayLast.year:
                dateRange= pd.Series(pd.date_range(dayFirst, dayFirst ,periods=1))
                dateRange[0] = dateRange[0].to_period('M')
                return dateRange
            else :
                dateRange = pd.Series(pd.date_range(dayFirst, dayLast ,freq='M'))
                for i in range(len(dateRange)):
                    dateRange[i]=dateRange[i].to_period('M')
                return dateRange        
    except:
          #trigger a generic error
          print("Error in date range generation")
          sys.exit(1)
      
        
def generateFinalDataFrame(dayFirst,dayLast,mode, data_folder):
    finalDataframe = pd.DataFrame()
    if mode=="Standard":
        lakeFile = data_folder / "lake.txt"
        finalDataframe = lakeData(lakeFile)
    elif mode == "Monthly":
        rangeDates = dateRangeGenerator(dayFirst,dayLast,mode)
        for i in range(len(rangeDates)):
            rangeDates[i]=rangeDates[i]
            fileName="lake-"+str(rangeDates[i])+".txt"
            lakeFile = data_folder / fileName
            compartments_prop_month = lakeData(lakeFile)
            compartments_prop_month["date"] = rangeDates[i]
            finalDataframe = finalDataframe.append(compartments_prop_month, ignore_index=True)
        
    return finalDataframe     