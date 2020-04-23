#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:04:19 2020

@author: vincentviguie
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

from declare_structures import *


def create_city_frame(grille:Grille_simulation,
                     land:Land_simulation,
                     trans:Transport_simulation,
                     ville:Etat_initial):
    """
    Transforme un jeu de variables "grille, land, trans,ville" en un dataframe.
    
    Usage: 
       df=create_city_frame(grille,land,trans,ville) 
       
       df : dataframe
       grille,land,trans,ville : les variables"""
    bb=np.vstack((grille.coord_X,
              grille.coord_Y,
              land.coeff_land,
              trans.prix_transport,
              ville.rent,
              ville.people,
              ville.housing,
              ville.hous))
    bb=bb.T #transposee 
    names=["coord_X",
           "coord_Y",
           "coeff_land",
           "prix_transport",
           "rent",
           "people",
           "housing",
           "hous"]
    df = pd.DataFrame(data=bb, index=None, columns=names)
    return df

def create_grid_simple(n):
    """Cree une grille de n*n pixels, centree en 0"""
    coord_X=np.zeros(n*n)
    coord_Y=np.zeros(n*n)

    indexu=0
    for i in range(n) :
        for j in range(n) :
            coord_X[indexu]=i-n/2
            coord_Y[indexu]=j-n/2
            indexu=indexu+1
    distance_centre=(coord_X**2+coord_Y**2) ** 0.5

    grille=Grille_simulation()
    grille.coord_X=coord_X
    grille.coord_Y=coord_Y
    grille.distance_centre=distance_centre
    grille.area=np.ones(n*n)
    
    return grille
    