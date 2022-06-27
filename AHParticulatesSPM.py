# -*- coding: utf-8 -*-
"""
Created on Thu May 26 14:43:52 2022

@author: alice
"""

import math
from GlobalConstants import *

from Particulates import Particulates #class to generate MP and SPM objects


#define ParticulatesSPM class (inheriting from Particulates class)
class AHParticulatesSPM(Particulates):
    "This is a class to create ParticulatesSPM objects" 
    
    #class attribute
    species = "particulate"
    
    #constructor
    def __init__(self, name, parentMP, parentSPM, NR_mps):
        self.name = name
        self.parentMP = parentMP
        self.parentSPM = parentSPM
        self.density_kg_m3 = parentMP.density_kg_m3*((NR_mps*parentMP.volume_m3)/((NR_mps*parentMP.volume_m3)+parentSPM.volume_m3))+parentSPM.density_kg_m3*(parentSPM.volume_m3/((NR_mps*parentMP.volume_m3)+parentSPM.volume_m3))        
        self.radius_m = (3*((NR_mps*parentMP.volume_m3)+parentSPM.volume_m3)/(4*math.pi))**(1/3)  #Note: this is an equivalent radius. MP-SPM most likely not truly spherical
        self.diameter_m = self.radius_m*2
        self.diameter_um = self.diameter_m*1e6
        
        self.composition = parentMP.composition + "-SPM"
        self.shape = parentMP.shape #to be updated for biofilm, could argue that shape is retained (unlike for SPM-bound)
                    

    
    #methods
    
    #volume calculation - currently simple version. 
    #more complexity to be added later:
    #different formulas for different particle shapes.
    #currently defined for spheres, fibres, cylinders, pellets and irregular fragments
    def calc_volume(self, parentMP, parentSPM):
        
        self.volume_m3 = parentMP.volume_m3 + parentSPM.volume_m3


    def calc_settling(self, settlingMethod, comp_depth_m):
        if settlingMethod == "Stokes":
            vSet_m_s = 2/9*(self.density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(self.radius_m)**2
        else: 
            print("Error: cannot calculate settling other than Stokes yet")
            #print error message settling methods other than Stokes 
            #(to be removed when other settling calculations are implemented)
        
    #for the water and surface water compartments:
    #settling and rising rate constants for free MP
        self.set_vel_m_s = vSet_m_s/comp_depth_m
        
        
    def calc_numConc(self, concMass_mg_L, concNum_part_L):
        
        if concNum_part_L == 0:
            self.concNum_part_m3 = concMass_mg_L/1000/self.density_kg_m3/self.volume_m3
            #if mass concentration is given, it is converted to number concentration
        else:
            self.concNum_part_m3 = concNum_part_L*1000
            #if number concentration is given, it is converted from part/L to part/m3
    