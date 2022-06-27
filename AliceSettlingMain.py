"""
Created on Thu May 19 23:16:14 2022

@author: alice
"""

#import relevant modules
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot as plt
sns.set()

#import file storing required constants
from GlobalConstants import *

#import modules from MAIN_MP_lake
from AHpreProcess import AHpreProcessHetero, Ratioplot, Heatdataframe
from readInputs import microplasticData
from Particulates import Particulates #class to generate MP and SPM objects

from pathlib import Path
data_folder = Path("inputs/") #insert folder containing input files


microplasticFile = data_folder / "AHplastics.txt"
plastic_prop = microplasticData(microplasticFile) 

#filling the dictionaries with particles and the name as key
MP_dict = {}
SPM_dict = {}
for index in range(len(plastic_prop)):
    
    name = plastic_prop.name[index]
    p = Particulates(plastic_prop, index)
    p.calc_volume()
    p.calc_settling('Stokes', comp_depth_m=1)
    if 'MP' in name:
        MP_dict[name] = p
    else:
        SPM_dict[name] = p


#making dictonary of heteroagregated particles
HA_dict = {}
for mp in MP_dict:
    mp_obj = MP_dict[mp]
    for spm in SPM_dict:
        spm_obj = SPM_dict[spm]
        
        HA_name = mp + '_' + spm
        pHA = AHpreProcessHetero(mp_obj,spm_obj)
        pHA.calc_settling('Stokes', comp_depth_m=1)
        HA_dict[HA_name] = pHA


################################################################################

#constants for which particles are used
ratio_SPM = 'SPM5'
bindings = 4
ratio_MP1 = 'MP3'
ratio_MP2 = 'MP8'
ratio_MP3 = 'MP13'
ratio_HA1 = ratio_MP1+'_'+ratio_SPM
ratio_HA2 = ratio_MP2+'_'+ratio_SPM
ratio_HA3 = ratio_MP3+'_'+ratio_SPM

#function that returns lists of the ratio of th HA and list of the velocity that is paired with it
[ratio_plot_1,vel_lit_1] = Ratioplot(MP_dict[ratio_MP1],SPM_dict[ratio_SPM], HA_dict[ratio_HA1], bindings)
[ratio_plot_2,vel_lit_2] = Ratioplot(MP_dict[ratio_MP2],SPM_dict[ratio_SPM], HA_dict[ratio_HA2], bindings)
[ratio_plot_3,vel_lit_3] = Ratioplot(MP_dict[ratio_MP3],SPM_dict[ratio_SPM], HA_dict[ratio_HA3], bindings)

#plotting the velocity
plt.plot(ratio_plot_1, vel_lit_1, label = ratio_MP1, c='r')
plt.plot(ratio_plot_2, vel_lit_2, label = ratio_MP2, c = 'g')
plt.plot(ratio_plot_3, vel_lit_3, label = ratio_MP3, c = 'b')
plt.title("SPM5, with a diameter of 100 µm")
plt.xlabel('Ratio MP to SPM (% heteroagregated) ')
plt.ylabel('Velocity m/s 10e-6')
plt.legend()
plt.show() 

################################################################################

#Making dataframe with that inlcude all the HA particles with one specific density of MP
df1 = Heatdataframe(HA_dict, 'Density-MP', 980)
df2 = Heatdataframe(HA_dict, 'Density-MP', 999)
df3 = Heatdataframe(HA_dict, 'Density-MP', 1580)

#plotting sublots for heatmap
fig, axes = plt.subplots(1, 3, sharey=True, figsize=(15,5))
fig.suptitle('Settling velocity of heteroaggregated particles by different MP densities')
axes[0].set_title('MP Density 980 kg/m^3 with velocity m/s')
axes[1].set_title('MP Density 999 kg/m^3 with velocity m/s')
axes[2].set_title('MP Density 1580 kg/m^3 with velocity m/s')

#plotting heatmap by making choosing the three variables
df1 = df1.sort_values(by=['MP_den'],ascending=False)
datatest = df1.pivot("SPM_dia","MP_dia", "HA_vel")
sns.heatmap(datatest, cbar=True, vmax=(None), vmin=(None), ax=axes[0])
axes[0].set_ylabel("SPM Diameter μm 10e-1")
axes[0].set_xlabel("MP Diameter μm 10e-1")

#plotting heatmap by making choosing the three variables
df2 = df2.sort_values(by=['MP_den'],ascending=False)
datatest = df2.pivot("SPM_dia","MP_dia", "HA_vel")
sns.heatmap(datatest, cbar=True, vmax=(None), vmin=(None), ax=axes[1])
axes[1].set_ylabel("SPM Diameter μm 10e-1")
axes[1].set_xlabel("MP Diameter μm 10e-1")

#plotting heatmap by making choosing the three variables
df3 = df3.sort_values(by=['MP_den'],ascending=False)
datatest = df3.pivot("SPM_dia","MP_dia", "HA_vel")
sns.heatmap(datatest, cbar=True, vmax=(None), vmin=(None), ax=axes[2])
axes[2].set_ylabel("SPM Diameter μm 10e-1")
axes[2].set_xlabel("MP Diameter μm 10e-1")

###############################################################################

#Making dataframe with that inlcude all the HA particles with one specific SPM
df4 = Heatdataframe(HA_dict, 'SPM', 'SPM1')
df5 = Heatdataframe(HA_dict, 'SPM', 'SPM2')
df6 = Heatdataframe(HA_dict, 'SPM', 'SPM3')
df7 = Heatdataframe(HA_dict, 'SPM', 'SPM4')
df8 = Heatdataframe(HA_dict, 'SPM', 'SPM5')

#plotting sublots for heatmap
fig, axes = plt.subplots(1, 5, sharey=True, figsize=(25,5))
fig.suptitle('Settling velocity of heteroaggregated particles by different SPM sizes')
axes[0].set_title('SPM 1 with diameter 1 µm')
axes[1].set_title('SPM 2 with diameter 3 µm')
axes[2].set_title('SPM 3 with diameter 10 µm')
axes[3].set_title('SPM 4 with diameter 30 µm')
axes[4].set_title('SPM 5 with diameter 100 µm')

#making the dataframes for the specific heatmap

df4 = df4.sort_values(by=['MP_den'],ascending=False)
datatest1 = df4.pivot("MP_den","MP_dia", "HA_vel")
sns.heatmap(datatest1, cbar=True, vmax=(None), vmin=(None), ax=axes[0])
axes[0].set_ylabel("MP Density kg/m^3")
axes[0].set_xlabel("MP Diameter μm 10e-1")

df5 = df5.sort_values(by=['MP_den'],ascending=False)
datatest2 = df5.pivot("MP_den","MP_dia", "HA_vel")
sns.heatmap(datatest2, cbar=True, vmax=(None), vmin=(None), ax=axes[1])
axes[1].set_ylabel("MP Density kg/m^3")
axes[1].set_xlabel("MP Diameter μm 10e-1")

df6 = df6.sort_values(by=['MP_den'],ascending=False)
datatest3 = df6.pivot("MP_den","MP_dia", "HA_vel")
sns.heatmap(datatest3, cbar=True, vmax=(None), vmin=(None), ax=axes[2])
axes[2].set_ylabel("MP Density kg/m^3")
axes[2].set_xlabel("MP Diameter μm 10e-1")

df7 = df7.sort_values(by=['MP_den'],ascending=False)
datatest4 = df7.pivot("MP_den","MP_dia", "HA_vel")
sns.heatmap(datatest4, cbar=True, vmax=(None), vmin=(None), ax=axes[3])
axes[3].set_ylabel("MP Density kg/m^3")
axes[3].set_xlabel("MP Diameter μm 10e-1")

df8 = df8.sort_values(by=['MP_den'],ascending=False)
datatest5 = df8.pivot("MP_den","MP_dia", "HA_vel")
sns.heatmap(datatest5, cbar=True, vmax=(None), vmin=(None), ax=axes[4])
axes[4].set_ylabel("MP Density kg/m^3")
axes[4].set_xlabel("MP Diameter μm 10e-1")

