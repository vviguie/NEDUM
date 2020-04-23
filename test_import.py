#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:50:56 2020

@author: vincentviguie
"""

import pandas as pd 
import numpy as np
import timeit #pour mesurer les temps
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sc
from scipy import optimize

#from rpy2.robjects import r, pandas2ri #interface entre R et python
#pandas2ri.activate()  #https://pandas.pydata.org/pandas-docs/version/0.22.0/r_interface.html

# https://cs231n.github.io/python-numpy-tutorial/#numpy

# %% data loading

print("\n*** city model ***\n")

from declare_structures import *
from basic_functions import *
from solveur_poly import *

param =	{
        "revenu" : 40000,
        "beta" : 0.3,
        "A" : 3,
        "b" : 0.6,
        "delta" : 0.05,
        "logit_poly" : 1,
        "coeff_land_max" : 0.62
}
#print(param)

grille=create_grid_simple(100)

path_data='/Users/vincentviguie/Documents/code/20 04 code charlotte 2/code_vincent/data/cities/'
city='Milan'

# %%
#grille
truc=pd.read_csv(path_data+city+'/Grid/grille_'+str.upper(city)+'_finale.csv')
truc2=pd.read_csv(path_data+city+'/Grid/Centre_'+str.upper(city)+'_final.csv')
distanceCBD = ((truc.XCOORD/1000 - truc2.X/1000)**2 + (truc.YCOORD/1000 - truc2.Y/1000)**2)**0.5

grille=Grille_simulation(truc.XCOORD/1000,
                         truc.YCOORD/1000,
                         distanceCBD,
                         truc.AREA/1000000)

#land
truc=pd.read_csv(path_data+city+'/Land_Cover/gridUrb_ESACCI_LandCover_2015_'+str.upper(city)+'.csv')
coeffUrbProp = param["coeff_land_max"]* (truc.OpenedToUrb / truc.TotalArea)
land=Land_simulation(coeffUrbProp)

carto2=lambda x: plt.scatter(grille.coord_X, grille.coord_Y, s=None, 
                             c=x,marker='.')

def carto3(x):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    
    ax.scatter(grille.coord_X, grille.coord_Y, x,
               c=x,alpha=0.2,marker='.')
    
    ax.set_xlabel('coord_X')
    ax.set_ylabel('coord_Y')
    ax.set_zlabel('Value')
    
    plt.show()


# %%
R_0 = 3000
population_cible=20000000

def compute_residual(R_0):
    ville=Etat_initial()
    ville.compute_ville(R_0,param,trans,land)
    population=ville.population
    F=population_cible-population
    return F

soluce=sc.optimize.fsolve(compute_residual,300)
ville=Etat_initial()
ville.compute_ville(soluce[0],param,trans,land)
print("R₀ vaut {}".format(soluce[0]))

# %% import data

rents_and_size=pd.read_csv(path_data+city+'/Real_Estate/GridData/'+str.upper(city)+'_rent.csv')
density=pd.read_csv(path_data+city+'/Population_Density/grille_GHSL_density_2015_'+str.upper(city)+'.txt')


data_gdp=pd.read_excel('/Users/vincentviguie/Documents/code/20 04 code charlotte 2/code_vincent/data/'+'gdp_capita_ppp.xlsx')
conversion_ppa=pd.read_csv('/Users/vincentviguie/Documents/code/20 04 code charlotte 2/code_vincent/data/'+'conversion_ppa.csv')

truc=pd.read_csv(path_data+city+'/Transport/interpDrivingTimesGoogle_'+str.upper(city)+'.csv')
truc2=pd.read_csv(path_data+city+'/Transport/interpTransitTimesGoogle_'+str.upper(city)+'.csv')

trans=Transport_simulation()
trans.create_trans_data(np.array(truc.Duration),np.array(truc2.Duration))



class Data_ville:  
    def __init__(self,
                 density=0,
                 totalPopulation=0,
                 medRent=0,
                 medSize=0,
                 totarea=0,
                 urb=0,
                 gdp_ppa=0,
                 conversion_ppa=0,
                 DistanceDriving=0,
                 DurationDriving=0,
                 DistanceTransit=0,
                 DurationTransit=0):
        self.density=density
        self.totalPopulation=totalPopulation
        self.medRent=medRent
        self.medSize=medSize
        self.totarea=totarea
        self.urb=urb
        self.gdp_ppa=gdp_ppa
        self.conversion_ppa=conversion_ppa
        self.DistanceDriving=DistanceDriving
        self.DurationDriving=DurationDriving
        self.DistanceTransit=DistanceTransit
        self.DurationTransit=DurationTransit
        
        
