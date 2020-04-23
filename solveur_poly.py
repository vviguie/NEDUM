#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:18:44 2020

@author: vincentviguie
"""

import pandas as pd 
import numpy as np
import timeit
import matplotlib.pyplot as plt
import scipy as sc

from declare_structures import *

class Centre_emplois:
    
    def __init__(self,x=0,y=0,nombre_job=1):
        """Constructeur de notre classe."""
        self.x=x
        self.y=y
        self.nombre_job=nombre_job

    def create_simple(self):
        """Cree un coeff_land uniforme qui vaut coeff."""
        self.x=np.array([0,0])
        self.y=np.array([0,10])
        self.nombre_job=np.array([2,1])
        
    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""
        return "Centre_emplois:\n  x: {}\n  y: {}\n  nombre_job: {}".format(
            self.x,self.y,self.nombre_job) 
    
    def create_simple_random(self,n,nombre_jobs,bas=0,haut=50):
        """Cree un coeff_land aleatoire de n centres d'emploi 
        entre les coord bas et haut."""
        
        self.x=np.random.random_integers(low=bas,high=haut, size=(n))
        self.y=np.random.random_integers(low=bas,high=haut, size=(n))
        self.nombre_job=nombre_jobs


def compute_poly(R_0,param,trans,land,poly):
    beta=param["beta"]
    alpha=1-beta
    revenu=param["revenu"]
    A=param["A"]
    b=param["b"]
    a=1-b
    delta=param["delta"]
    logit_poly=param["logit_poly"]
    
    #R_0=np.exp(R_0)

    # revenu minus transport, or 0 if it is negative
    revenu_minus_transport_positive=np.fmax(
        revenu-trans.prix_transport,np.zeros(trans.prix_transport.shape)
        )

    bid_rent= (R_0* 
           revenu_minus_transport_positive**(1/beta)
           /revenu**(1/beta)
           )
    
    rent=np.amax(bid_rent,axis=-1)
    quel=np.argmin(bid_rent, axis=-1)
   
    # %%  calcul proba
    rent_repete=np.tile(rent,(len(poly.x),1))
    rent_repete=rent_repete.T
    
    #pour enlever le warning quand on divise par 0
    np.seterr(divide='ignore', invalid='ignore')
    proba=np.exp(
        (bid_rent
        -rent_repete)
        /bid_rent)
    proba[bid_rent==0]=0
    
    proba=np.reshape(poly.nombre_job,(1,-1))*proba
    proba=proba/np.reshape(np.sum(proba,axis=1),(-1,1))
    
    proba[np.isnan(proba)]=0

    #pour le remettre pour la suite du code
    np.seterr(divide='warn', invalid='warn')
    
    # proba_log=((
    #     rent_repete
    #     -bid_rent)/rent_repete)
    # proba_log=proba_log-np.log(np.reshape(np.sum(np.exp(proba),axis=1),(-1,1)))
    # proba3=np.exp(proba_log)
    # %%
    
    #pour enlever le warning quand on divise par 0
    np.seterr(divide='ignore', invalid='ignore')
    hous = beta * np.amax(revenu_minus_transport_positive,axis=-1) /rent
    #pour le remettre pour la suite du code
    np.seterr(divide='warn', invalid='warn')
    hous[np.isnan(hous)]=0

    #housing=A*rent.^(1/b)/delta.*land.coeff_land
    housing=(A**(1/a))*((b/delta*rent)**(b/a))
    
    #pour enlever le warning quand on divise par 0
    np.seterr(divide='ignore', invalid='ignore')
    people = housing / hous
    #pour le remettre pour la suite du code
    np.seterr(divide='warn', invalid='warn')
    
    people[np.isnan(people)]=0

    LOGIT=1
    if LOGIT:
        people_travaille=np.reshape(people*land.coeff_land,(-1,1))*proba
    else:
        #if no logit
        people_travaille=np.tile(people*land.coeff_land,(len(poly.x),1))
        people_travaille=people_travaille.T
        
        masque=np.zeros(people_travaille.shape)
        masque[range(len(quel)),quel]=1
        
        people_travaille=people_travaille*masque
    
    #population=np.sum(people*land.coeff_land.reshape(-1,1),axis=0)
    population=np.sum(people_travaille)
    
    #'cet sca que l'on met dans la variable de sortie population
    nombre_job=np.sum(people_travaille,axis=0)

    ville=Etat_initial()
    ville.population=nombre_job
    ville.rent=rent
    ville.hous=hous
    ville.housing=housing
    ville.people=people
    ville.R_0=R_0
    ville.people_travaille=people_travaille
    
    return ville
    
def create_trans_simple_poly(prix_transport_par_km,grille:Grille_simulation,poly):
    
    x_jobs=poly.x.reshape(1,-1)
    y_jobs=poly.y.reshape(1,-1)  

    coord_X=grille.coord_X.reshape(-1,1)
    coord_Y=grille.coord_Y.reshape(-1,1)  
    
    distances_to_jobs=((coord_X-x_jobs)**2+(coord_Y-y_jobs)**2)**(0.5)
    
    prix_VP=distances_to_jobs*prix_transport_par_km

    prix_TC=float('Inf')*np.ones(prix_VP.shape)
    
    tous_prix=np.stack((prix_VP,prix_TC),axis=-1)#les prix concaténés
    prix_transport=np.amin(tous_prix, axis=-1)
    mode=np.argmin(tous_prix, axis=-1)

    trans=Transport_simulation()
    trans.prix_transport_par_km=prix_transport_par_km
    trans.prix_VP=prix_VP
    trans.prix_TC=prix_TC
    trans.mode=mode
    trans.prix_transport=prix_transport
    
    return trans