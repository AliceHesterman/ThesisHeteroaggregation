# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:14:22 2022

@author: alice
"""


from AHParticulatesSPM import AHParticulatesHA

from RC_Generator import settling
import pandas as pd

def AHpreProcessHetero(MP,SPM):
    #make a HA particulate
    x = AHParticulatesHA("{}-{}".format(str(MP.name),str(SPM.name)), MP, SPM, 1) 
    x.calc_volume(MP, SPM)
    return x

def Ratioplot(MP,SPM, MP_SPM, amount_HA):
    
    #calculate the settling velocity
    comp_depth_m = 1
    spmV = settling(SPM.density_kg_m3, SPM.radius_m, comp_depth_m, "Stokes")
    mp_spmV = settling(MP_SPM.density_kg_m3, MP_SPM.radius_m, comp_depth_m, "Stokes")
    
    #making list of the HA particulates and the corresponding velocity
    list_HA = [SPM,MP_SPM]
    list_VelHA = [spmV,mp_spmV]
    for i in range(2,amount_HA+2):
        MP_SPM_HA = AHParticulatesHA(MP_SPM.name + "_HA" + str(i), MP, SPM, i)
        list_HA.append(MP_SPM_HA)
        list_VelHA.append(settling(MP_SPM_HA.density_kg_m3, MP_SPM_HA.radius_m, comp_depth_m, "Stokes"))
    
    #making list of the velocity that correspond with the list of ratio that is present of HA particles
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
            
    return [ratio_list, vel_list]

def Heatdataframe(HA_dict, var_check, var):
    #makes a dataframe with only the specific variable
    
    HA_name = []
    MP_name = []
    MP_dia = []
    MP_den = []
    MP_vel = []
    SPM_name = []
    SPM_dia = []
    SPM_den = []
    SPM_vel = []
    HA_vel = []
    HA_den = []
    HA_dia = []

    for ha in HA_dict:
        ha_obj = HA_dict[ha]
        if var_check == 'Density-MP':
            if var != int(ha_obj.parentMP.density_kg_m3):
                continue
        elif var_check == 'SPM':
            if var != ha_obj.parentSPM.name:
                continue
        HA_name.append(ha_obj.name)
        
        MP_name.append(ha_obj.parentMP.name)
        MP_dia.append(round(ha_obj.parentMP.diameter_m*10**7))
        MP_den.append(ha_obj.parentMP.density_kg_m3)
        MP_vel.append(ha_obj.parentMP.set_vel_m_s)
        
        SPM_name.append(ha_obj.parentSPM.name)
        SPM_dia.append(round(ha_obj.parentSPM.diameter_m*10**7))
        SPM_den.append(ha_obj.parentSPM.density_kg_m3)
        SPM_vel.append(ha_obj.parentSPM.set_vel_m_s)

        HA_vel.append(ha_obj.set_vel_m_s)
        HA_den.append(ha_obj.density_kg_m3)
        HA_dia.append(ha_obj.diameter_m)

    df = pd.DataFrame({'HA_name':HA_name,
                       'MP_name':MP_name,
                          'MP_dia':MP_dia,
                          'MP_den':MP_den,
                          'SPM_name':SPM_name,
                          'SPM_dia':SPM_dia,
                          'SPM_den':SPM_den,
                          'HA_vel':HA_vel,
                          'HA_den':HA_den,
                          'HA_dia':HA_dia})
    return df