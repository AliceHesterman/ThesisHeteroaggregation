"""
Created on Thu May 19 23:16:14 2022

@author: alice
"""





#import relevant modules
import os
import math
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd
from plots import finalPlotting
from collections import defaultdict
import seaborn as sns


from AHpreProcess import AHpreProcessPlatics,AHpreProcessHetero, Ratioplot

from readInputs import lakeData,dateRangeGenerator,microplasticData, processData, generateFinalDataFrame, processDailyInputData
from datetime import datetime, timedelta

from pathlib import Path
data_folder = Path("inputs/") #insert folder containing input files

#import file storing required constants
from GlobalConstants import *


#import classes to generate objects
from Particulates import Particulates #class to generate MP and SPM objects
from ParticulatesSPM import ParticulatesSPM #class to generate MP and SPM objects

#from EnvCompartment import EnvCompartment #class to generate environmental 
#compartment objects (water, water surface, sediment)

from RC_Generator import settling
import fillRCmatrix 

skip = []

ratio_MP = 'MP5'
ratio_SPM = 'SPM1'
bindings = 4


ratio_HA = ratio_MP+'_'+ratio_SPM


microplasticFile = data_folder / "AHplastics.txt" # Eigen Data in ander .txt formaat doen
plastic_prop = microplasticData(microplasticFile) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#currently also contains SPM properties, might need to move those to separate file

MP_dict = {}
SPM_dict ={}


for index in range(len(plastic_prop)):

    
    name = plastic_prop.name[index]
    if name in skip:
        continue
    p = Particulates(plastic_prop, index)
    p.calc_volume()
    p.calc_settling('Stokes', comp_depth_m=1)
    if 'MP' in name:
        MP_dict[name] = p
    else:
        SPM_dict[name] = p

HA_dict = {}

for mp in MP_dict:
    mp_obj = MP_dict[mp]
    for spm in SPM_dict:
        spm_obj = SPM_dict[spm]
        
        HA_name = mp + '_' + spm
        pHA = AHpreProcessHetero(mp_obj,spm_obj)
        pHA.calc_settling('Stokes', comp_depth_m=1)
        HA_dict[HA_name] = pHA


Ratioplot(MP_dict[ratio_MP],SPM_dict[ratio_SPM], HA_dict[ratio_HA], bindings)

'''
HA_name = []
MP_name = []
MP_rad = []
MP_den = []
MP_vel = []
SPM_name = []
SPM_rad = []
SPM_den = []
SPM_vel = []
HA_vel = []
HA_den = []
HA_rad = []

which_heat_var = 980

for ha in HA_dict:
    ha_obj = HA_dict[ha]
    if which_heat_var != int(ha_obj.parentMP.density_kg_m3):
            continue
    #if which_heat_spm not in ha_obj.parentMP.name:
    #   continue
    HA_name.append(ha_obj.name)
    
    MP_name.append(ha_obj.parentMP.name)
    MP_rad.append(round(ha_obj.parentMP.radius_m*10**9))
    MP_den.append(ha_obj.parentMP.density_kg_m3)
    MP_vel.append(ha_obj.parentMP.set_vel_m_s)
    
    SPM_name.append(ha_obj.parentSPM.name)
    SPM_rad.append(round(ha_obj.parentSPM.radius_m*10**9))
    SPM_den.append(ha_obj.parentSPM.density_kg_m3)
    SPM_vel.append(ha_obj.parentSPM.set_vel_m_s)

    HA_vel.append(ha_obj.set_vel_m_s)
    HA_den.append(ha_obj.density_kg_m3)
    HA_rad.append(ha_obj.radius_m)
    
y=HA_name
x1=MP_vel
x2=SPM_vel
x3=HA_vel

plt.scatter(x1,y,c="red",label='MP')
plt.scatter(x2,y,c="green",label='SPM')
plt.scatter(x3,y,c="blue",label='HA')
plt.xlabel("X")
plt.tick_params(axis='x', which='major')
plt.ylabel("Y")
plt.title("Scatter Plot of two different datasets")
plt.legend()
plt.show()
         
       
'''

df = pd.DataFrame({'HA_name':HA_name,
                   'MP_name':MP_name,
                      'MP_rad':MP_rad,
                      'MP_den':MP_den,
                      'SPM_name':SPM_name,
                      'SPM_rad':SPM_rad,
                      'SPM_den':SPM_den,
                      'HA_vel':HA_vel,
                      'HA_den':HA_den,
                      'HA_rad':HA_rad})
    
    
df = df.sort_values(by=['MP_den'],ascending=False)
    
datatest = df.pivot("SPM_rad","MP_rad", "HA_vel")
ax = sns.heatmap(datatest, cbar=True, vmax=(None), vmin=(None))

df.to_csv('test1.csv', index=False)
    


df2 = pd.DataFrame(data={'MP_name':MP_name,
                             'MP':MP_rad,
                             'HA_vel':HA_vel})

#Ratioplot(MP3,SPM1, MP3_SPM1)
#Ratioplot(MP3,SPM1, MP3_SPM1)

#df.to_csv('test.csv', index=False)

'''




'''
[MP1,MP2,MP3,SPM1,SPM2,SPM3,SPM4,SPM5] = AHpreProcessPlatics(plastic_prop)


MP1_SPM1 = AHpreProcessHetero(MP1,SPM1)
MP2_SPM1 = AHpreProcessHetero(MP2,SPM1)
MP3_SPM1 = AHpreProcessHetero(MP3,SPM1)
MP1_SPM2 = AHpreProcessHetero(MP1,SPM2)
MP2_SPM2 = AHpreProcessHetero(MP2,SPM2)
MP3_SPM2 = AHpreProcessHetero(MP3,SPM2)
MP1_SPM3 = AHpreProcessHetero(MP1,SPM3)
MP2_SPM3 = AHpreProcessHetero(MP2,SPM3)
MP3_SPM3 = AHpreProcessHetero(MP3,SPM3)
MP1_SPM4 = AHpreProcessHetero(MP1,SPM4)
MP2_SPM4 = AHpreProcessHetero(MP2,SPM4)
MP3_SPM4 = AHpreProcessHetero(MP3,SPM4)
MP1_SPM5 = AHpreProcessHetero(MP1,SPM5)
MP2_SPM5 = AHpreProcessHetero(MP2,SPM5)
MP3_SPM5 = AHpreProcessHetero(MP3,SPM5)

list_HA1 = [MP1_SPM1,MP2_SPM1,MP3_SPM1,MP1_SPM2,MP2_SPM2,MP3_SPM2,MP1_SPM3,MP2_SPM3,MP3_SPM3,MP1_SPM4,MP2_SPM4,MP3_SPM4,MP1_SPM5,MP2_SPM5,MP3_SPM5]
list_mp = [MP1,MP2,MP3]
list_spm = [SPM1,SPM2,SPM3,SPM4,SPM5]

list_Psetv = []
list_Pnames = []

for p in list_HA1:
    list_Pnames.append(p.name)

comp_depth_m = 1

for p in list_HA1:
    setv = settling(p.density_kg_m3, p.radius_m, comp_depth_m, "Stokes")
    list_Psetv.append(setv)
    
VMP1 = settling(MP1.density_kg_m3, MP1.radius_m, comp_depth_m, "Stokes")
VMP2 = settling(MP2.density_kg_m3, MP2.radius_m, comp_depth_m, "Stokes")
VMP3 = settling(MP3.density_kg_m3, MP3.radius_m, comp_depth_m, "Stokes")

VSPM1 = settling(SPM1.density_kg_m3, SPM1.radius_m, comp_depth_m, "Stokes")
VSPM2 = settling(SPM2.density_kg_m3, SPM2.radius_m, comp_depth_m, "Stokes")
VSPM3 = settling(SPM3.density_kg_m3, SPM3.radius_m, comp_depth_m, "Stokes")    
VSPM4 = settling(SPM4.density_kg_m3, SPM4.radius_m, comp_depth_m, "Stokes") 
VSPM5 = settling(SPM5.density_kg_m3, SPM5.radius_m, comp_depth_m, "Stokes") 
    


plt.scatter(list_names, list_setv, c='r')
plt.xlabel('Particles')
plt.ylabel('Velocity')
plt.title('Particles settling Velocity')
plt.show()
'''



############
# Plot ze allemaal.
'''
