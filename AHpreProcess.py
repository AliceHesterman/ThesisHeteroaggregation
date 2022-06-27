# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:14:22 2022

@author: alice
"""

from Particulates import Particulates #class to generate MP and SPM objects
from ParticulatesBF import ParticulatesBF #class to generate MP and SPM objects
from ParticulatesSPM import ParticulatesSPM #class to generate MP and SPM objects
from AHParticulatesSPM import AHParticulatesSPM

from RC_Generator import settling
import matplotlib.pyplot as plt
import pandas as pd

def AHpreProcessPlatics(plastic_prop):
    #generate MicroPlastic object(s) --> A: pristine (free MP)
    MP1_index = 0 
    MP2_index = 1
    MP3_index = 2

    MP1= Particulates(plastic_prop, MP1_index)
    MP1.calc_volume()
    
    MP2= Particulates(plastic_prop, MP2_index)
    MP2.calc_volume()
    
    MP3= Particulates(plastic_prop, MP3_index)
    MP3.calc_volume()
        
    #generate SPM object(s)
    SPM1_index = 3 #need to move SPM in own input file
    SPM2_index = 4
    SPM3_index = 5
    SPM4_index = 6
    SPM5_index = 7
    
    SPM1 = Particulates(plastic_prop, SPM1_index)
    SPM1.calc_volume()
    
    SPM2 = Particulates(plastic_prop, SPM2_index)
    SPM2.calc_volume()
    
    SPM3 = Particulates(plastic_prop, SPM3_index)
    SPM3.calc_volume()
    
    SPM4 = Particulates(plastic_prop, SPM4_index)
    SPM4.calc_volume()
    
    SPM5 = Particulates(plastic_prop, SPM5_index)
    SPM5.calc_volume()    
    #SPM1.calc_numConc(50, 0) #move this to lake input file ###????
    
    return MP1,MP2,MP3,SPM1,SPM2,SPM3,SPM4,SPM5

def AHpreProcessHetero(MP,SPM):
    #x = ParticulatesSPM("{}-{}".format(str(MP.name),str(SPM.name)), MP, SPM) 
    #x.calc_volume(MP, SPM)
    
    x = AHParticulatesSPM("{}-{}".format(str(MP.name),str(SPM.name)), MP, SPM, 1) 
    x.calc_volume(MP, SPM)
    return x

def Ratioplot(MP,SPM, MP_SPM, amount_HA):
    comp_depth_m = 1
    mpV = settling(MP.density_kg_m3, MP.radius_m, comp_depth_m, "Stokes")
    spmV = settling(SPM.density_kg_m3, SPM.radius_m, comp_depth_m, "Stokes")
    mp_spmV = settling(MP_SPM.density_kg_m3, MP_SPM.radius_m, comp_depth_m, "Stokes")
    
    list_HA = [SPM,MP_SPM]
    list_VelHA = [spmV,mp_spmV]

    for i in range(2,amount_HA+2):
        MP_SPM_HA = AHParticulatesSPM(MP_SPM.name + "_HA" + str(i), MP, SPM, i)
        list_HA.append(MP_SPM_HA)
        list_VelHA.append(settling(MP_SPM_HA.density_kg_m3, MP_SPM_HA.radius_m, comp_depth_m, "Stokes"))
    
    vel_list = []
    ratio_list = []
    
    for k in range(0,len(list_HA)-1):
        begin_SPM = list_HA[k]
        eind_SPM = list_HA[k+1]
        
        vel_begin_t = settling(begin_SPM.density_kg_m3, begin_SPM.radius_m, comp_depth_m, "Stokes")
        vel_eind_t = settling(eind_SPM.density_kg_m3, eind_SPM.radius_m, comp_depth_m, "Stokes")
        
        for n in range (0,100):
            
            vel_eind = vel_eind_t * n
            vel_begin = vel_begin_t * (100-n)
            V_total = (vel_begin + vel_eind)/100
            vel_list.append(V_total)
            ratio_list.append(n+(100*k))
            
    plt.plot(ratio_list, vel_list, c='r')
    plt.xlabel('Ratio, % heteroagregated compared to SPM')
    plt.ylabel('Velocity')
    plt.title('Particles settling Velocity')
    plt.show()
    return 0

Velocity('SPM1')
