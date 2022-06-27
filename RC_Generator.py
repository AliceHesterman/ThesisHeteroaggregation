# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:49:15 2019

@author: AntoniaPraetorius
"""

#module containing functions to calculate all rate constants

import math

#import file storing required constants
from GlobalConstants import *

    
    
    
def degradation(t_half_d):
    
    #degradation estimations
    """ relates only to MP & NPs. Full degradation probably extremely slow
    possibly not significant for most simulations. But add anyway for scenario
    analysis or biodegradable polymers. Values currently placeholders
    ! Add a size relation?!"""
    #degradation half-life of MPs used as input is in days
        
    #degradation rate constant 
    k_deg = math.log(2)/(t_half_d*24*60*60) 

    return k_deg

    #fragmentation estimations
    """ relates only to MP & NPs. Data scarce. Need to investiage more to get 
    numbers. Current values/pathways are placeholders for later. Currently 
    assume fragmentation only in water
    current function works only for 5 size bin and fragmentation from one
    size to the next smaller size bin. Need to calculate how many fragments are 
    created from next bigger size and estimate time that takes
    """
    
def fragmentation(k_frag_gen_d, MP_radius_m, MP_volume_m3, MP_diameter_um):
    #fragmentation estimations
    """ relates only to MP & NPs. Data scarce. Need to investiage more to get 
    numbers. Current values/pathways are placeholders for later. Currently 
    assume fragmentation only in water
    current function works only for 5 size bin and fragmentation from one
    size to the next smaller size bin. Need to calculate how many fragments are 
    created from next bigger size and estimate time that takes
    """
    #input k_frag_d & k_frag_gen_ws_d is generic fragmentation rate
    #constant describing how many MP fragment per day. To be scaled with a
    #size factor to create size dependence
    #fragmentation in water surface (ws) assumed to be faster in 
    #main water (w1)
        
    #estimate fragmentation relation between size bins
    volume_fragment = 4/3*math.pi*(MP_radius_m/10)**3 #!!!only works for bins 10 times smaller!!!
    fragments_formed = MP_volume_m3/volume_fragment
    k_frag = k_frag_gen_d*MP_diameter_um/1000/24/60/60
    
    #NOTE: check this again!!
    
    return k_frag


def settling(MP_density_kg_m3, MP_radius_m, comp_depth_m, settlingMethod):
    #settling calculations
    """settling can be calculated using different equations (e.g. Stokes, 
    modified versions of it or others) or be taken from experimental studies
    !! currently only classical Stokes is implemented (which is probably not 
    very realistic and will be updated soon !!""" 
 
    if settlingMethod == "Stokes":
        vSet_m_s = 2/9*(MP_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(MP_radius_m)**2
    else: 
        print("Error: cannot calculate settling other than Stokes yet")
        #print error message settling methods other than Stokes 
        #(to be removed when other settling calculations are implemented)
        
    #for the water and surface water compartments:
    #settling and rising rate constants for free MP
    k_set = vSet_m_s/comp_depth_m
    '''
    if vSet_m_s > 0:
        k_set = vSet_m_s/comp_depth_m
            
    elif vSet_m_s  < 0:
        k_set  = 0
        
    else:
        k_set  = 0
'''        
    return k_set


def rising(MP_density_kg_m3, MP_radius_m, comp_depth_m, settlingMethod):
    #rising calculations
    """rising is calculated in the same way as settling for particles with negative 
    settling velocitis. 
    It can be calculated using different equations (e.g. Stokes, 
    modified versions of it or others) or be taken from experimental studies
    !! currently only classical Stokes is implemented (which is probably not 
    very realistic and will be updated soon !!""" 
 
    if settlingMethod == "Stokes":
        vSet_m_s = 2/9*(MP_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(MP_radius_m)**2
    else: 
        print("Error: cannot calculate settling other than Stokes yet")
        #print error message settling methods other than Stokes 
        #(to be removed when other settling calculations are implemented)
        
    #for the water and surface water compartments:
    #settling and rising rate constants for free MP
    if vSet_m_s > 0:
        k_rise = 0
            
    elif vSet_m_s  < 0:
        k_rise = -vSet_m_s/comp_depth_m
        
   # else:
        k_rise  = 0
        
    return k_rise

def heteroagg(alpha, MP_radius_m, SPM_radius_m, MP_density_kg_m3, SPM_density_kg_m3, SPM_concNum_part_m3, G, T_K):
    
    #heteroaggregation rate constants
    """heteroaggregation requires to particles to collide and interact
    favorably for the collision to result in attachment
    the heteroaggregation rate constants is therefore composed of two
    parts, 1) a collision rate constant and 2) and attachement 
    efficiency (alpha) (representing the probability of attachement).
    For heteroaggregation a common simplifaction is the assumption that
    SPM concentration is not signficantly affected by the heteroaggre-
    gation process. Therefore, a pseudo first-order heteroaggregation 
    rate constant is obtained by multiplying collision rate with alpha 
    and with the SPM number concentration"""
    
    #first the different collision mechanisms are calculated
    k_peri = (2*k_B_J_K*T_K)/(3*mu_w_21C_kg_ms)*(MP_radius_m + SPM_radius_m)**2/(MP_radius_m * SPM_radius_m)
    #perikinetic contributions to collision rate constant (Brownian motion)
    
    k_ortho = 4/3*G*(MP_radius_m + SPM_radius_m)**3
    #orthokinetic contributions to collision rate constant (caused by fluid motion)
    
    MP_vSet_m_s = 2/9*(MP_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(MP_radius_m)**2
    SPM_vSet_m_s = 2/9*(SPM_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(SPM_radius_m)**2
    #settling velocity. currently according to classical Stokes law. Need to include other modes and put calculation on its own, so that it can also be accessed for other processes
    
    k_diffSettling = math.pi*(MP_radius_m + SPM_radius_m)**2 * abs(MP_vSet_m_s-SPM_vSet_m_s)
    #differential settling contributions to collision rate constant

    k_coll = k_peri + k_ortho + k_diffSettling
    #the collision rate constant
    
    k_hetAgg = alpha*k_coll*SPM_concNum_part_m3
    #the pseudo first-order heteroaggregation rate constant
        
    
    return k_hetAgg


def breakup(alpha, MP_radius_m, SPM_radius_m, MP_density_kg_m3, SPM_density_kg_m3, SPM_concNum_part_m3, G, T_K):

             #data is limited on aggregate breakup, but this process is likely
            #more relvant for larger aggregates
            #!! 1/10 of k_hetAgg is just a placeholder,  needs to be refined
            #possibly using a size dependent function !!
            #first the different collision mechanisms are calculated
    k_peri = (2*k_B_J_K*T_K)/(3*mu_w_21C_kg_ms)*(MP_radius_m + SPM_radius_m)**2/(MP_radius_m * SPM_radius_m)
    #perikinetic contributions to collision rate constant (Brownian motion)
    
    k_ortho = 4/3*G*(MP_radius_m + SPM_radius_m)**3
    #orthokinetic contributions to collision rate constant (caused by fluid motion)
    
    MP_vSet_m_s = 2/9*(MP_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(MP_radius_m)**2
    SPM_vSet_m_s = 2/9*(SPM_density_kg_m3-density_w_21C_kg_m3)/mu_w_21C_kg_ms*g_m_s2*(SPM_radius_m)**2
    #settling velocity. currently according to classical Stokes law. Need to include other modes and put calculation on its own, so that it can also be accessed for other processes
    
    k_diffSettling = math.pi*(MP_radius_m + SPM_radius_m)**2 * abs(MP_vSet_m_s-SPM_vSet_m_s)
    #differential settling contributions to collision rate constant

    k_coll = k_peri + k_ortho + k_diffSettling
    #the collision rate constant
    
    k_hetAgg = alpha*k_coll*SPM_concNum_part_m3
    #the pseudo first-order heteroaggregation rate constant

    k_aggBreakup = 1/10*k_hetAgg
    
    return k_aggBreakup


def advection(compType, comp_volume_m3):
    #advective transport
    #currently  based on assumption of total residence time of lake 
    #water to be 2 years (Bogdal 2010 lake model)
    #!! will be revised!!
    if compType == "water":
        k_adv = comp_volume_m3/(2*365*24*60*60) 
    
    if compType == "surface":
        k_adv = comp_volume_m3/(2*365*24*60*60) 
        
    return k_adv


def mixing(compartment, Epilimnion, updown="mixdir"):
    
    if compartment.name == "epilimnion":
        if updown == "up":
            k_mix = 10e-10 #random number, need to refine!!
        if updown == "down":
            k_mix = 10e-13 #random number, need to refine!!
        
    if compartment.name == "surface":
        k_mix = 10e-10*(Epilimnion.volume_m3/compartment.volume_m3)
    
    if compartment.name == "hypolimnion":
        k_mix = 10e-13*(Epilimnion.volume_m3/compartment.volume_m3)
          
    if compartment.name == "sediment":
        k_mix = 0
          
    return k_mix



def biofilm(compartment, process_prop):
    
    if compartment.name == "surface":
        if process_prop.t_biof_growth_d[0] == 0:
            k_biof = 0
        else:
            k_biof = 1/process_prop.t_biof_growth_d[0]/24/60/60
        
    if compartment.name == "epilimnion":
        if process_prop.t_biof_growth_d[1] == 0:
            k_biof = 0
        else:
            k_biof = 1/process_prop.t_biof_growth_d[1]/24/60/60
    
    if compartment.name == "hypolimnion":
        if process_prop.t_biof_growth_d[2] == 0:
            k_biof = 0
        else:
            k_biof = 1/process_prop.t_biof_growth_d[2]/24/60/60
    
    if compartment.name == "sediment":
        k_biof = 0
    
    #assume it takes x days for biofilm coverage to grow
    #need to update!!
    
    return k_biof



#for the sediment compartment rate constants for resuspension and
            #burial in deep sediment are calculated & degradation rate assigned

def resusp(compartment):
    k_resusp = 2.3*10**-7/compartment.depth_m
    
    return k_resusp



def burial(compartment):
    k_burial = 5.6*10**-7/compartment.depth_m
    
    return k_burial

