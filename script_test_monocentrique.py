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
import scipy as sc
from scipy import optimize

#from rpy2.robjects import r, pandas2ri #interface entre R et python
#pandas2ri.activate()  #https://pandas.pydata.org/pandas-docs/version/0.22.0/r_interface.html

# https://cs231n.github.io/python-numpy-tutorial/#numpy

# %% data loading

print("\n*** city model ***\n")

from declare_structures import *
from basic_functions import *

param =	{
        "revenu" : 40000,
        "beta" : 0.3,
        "A" : 3,
        "b" : 0.6,
        "delta" : 0.05
}
#print(param)

# grille=Grille_simulation()
# grille.create_grid(100)

grille=create_grid_simple(100)

land=Land_simulation()
land.create_land_unif(grille,1)

land2=Land_simulation()
land2.create_land_unif(grille,0.9)

trans=Transport_simulation()
trans.create_trans_simple(2*365,grille)
trans_metro=Transport_simulation()
trans_metro.create_trans_metro(2*365,grille)

R_0 = 3000
population_cible=20000000

# %% fonction de figure rapide

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

# %% simulation

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


def compute_residual(R_0):
    ville=Etat_initial()
    ville.compute_ville(R_0,param,trans_metro,land)
    population=ville.population
    F=population_cible-population
    return F

soluce2=sc.optimize.fsolve(compute_residual,300)
ville_metro=Etat_initial()
ville_metro.compute_ville(soluce2[0],param,trans_metro,land)
print("R₀ vaut {}".format(soluce2[0]))

# %% cartes
a_tracer=(ville_metro.rent-ville.rent)/(ville_metro.rent+ville.rent)
#a_tracer=(ville_metro.rent>0)
#a_tracer[np.isnan(a_tracer)]=0
carto3(a_tracer)
#plt.scatter(grille.distance_centre,ville.rent)

# %% test dataframe

testi=create_city_frame(grille,land,trans,ville)



