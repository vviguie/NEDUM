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
        "logit_poly" : 1
}
#print(param)

# grille=Grille_simulation()
# grille.create_grid(100)

grille=create_grid_simple(100)

land=Land_simulation()
land.create_land_unif(grille,1)

land2=Land_simulation()
land2.create_land_unif(grille,0.9)


n=2

population_cible=(np.array(range(1,n+1))*1000000)
R_0=(population_cible/10000)

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


poly=Centre_emplois()
#poly.create_simple()
poly.create_simple_random(n,population_cible/1000000,-25,25)

trans=create_trans_simple_poly(2*365,grille,poly)

#ville2=compute_poly(np.array([300,200]),param,trans,land,poly)


def compute_residual(R_0):
    ville=compute_poly(R_0,param,trans,land,poly)
    population=ville.population
    F=population_cible-population
    return F


# %%
soluce=sc.optimize.fsolve(compute_residual,R_0,full_output=0)
#print(soluce)

ville=compute_poly(soluce,param,trans,land,poly)
carto3(ville.rent)
print(compute_residual(soluce))


# %%
path_data='/Users/vincentviguie/Documents/code/20 04 code charlotte 2/code_vincent/data/cities/'

# %%
city='Milan'
truc=pd.read_csv(path_data+city+'/Grid/grille_'+str.upper(city)+'_finale.csv')


truc.coord_X
truc.coord_Y
truc.distance_centre

#grid.ID = ID
#grid.xCoord = XCOORD/1000
#grid.yCoord = YCOORD/1000
#grid.sizeSquare = sqrt(AREA') / 1000; % in km

