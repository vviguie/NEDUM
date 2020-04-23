#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:17:52 2020

@author: vincentviguie
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt



class classe_vide:
    pass

class Grille_simulation:
    """Classe définissant une grille caractérisée par :
    - coord_X
    - coord_Y
    - distance_centre"""
    
    def __init__(self,coord_X=0,coord_Y=0,distance_centre=0,area=0): # Notre méthode constructeur
        """Constructeur de notre classe"""
        self.coord_X = coord_X
        self.coord_Y=coord_Y
        self.distance_centre=distance_centre
        self.area=area
        
        
    def create_grid(self,n):
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
    
        self.coord_X=coord_X
        self.coord_Y=coord_Y
        self.distance_centre=distance_centre
        self.area=1

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""
        return "Grid:\n  coord_X: {}\n  coord_Y: {}\n  distance_centre: {}\n  area: {}".format(
                self.coord_X, self.coord_Y, self.distance_centre,self.area)             
  


class Land_simulation:
    
    def __init__(self,coeff_land=0):
        """Constructeur de notre classe."""
        self.coeff_land=coeff_land

    def create_land_unif(self,grille:Grille_simulation,coeff):
        """Cree un coeff_land uniforme qui vaut coeff."""
        coeff_land=np.ones(len(grille.coord_X))*coeff

        self.coeff_land=coeff_land
        
    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""
        return "Land:\n  coeff_land: {}".format(
            self.coeff_land) 
    
    
class Transport_simulation:
    
    def __init__(self,prix_transport_par_km=0,prix_VP=0,prix_TC=0,mode=0,prix_transport=0):
        self.prix_transport_par_km=prix_transport_par_km
        self.prix_VP=prix_VP
        self.prix_TC=prix_TC
        self.mode=mode
        self.prix_transport=prix_transport
        
    def create_trans_metro(self,prix_transport_par_km,grille:Grille_simulation):
        
        prix_VP=grille.distance_centre*prix_transport_par_km
    
        prix_TC=float('Inf')*np.ones(len(prix_VP)) #prix_TC is equal to infinity, i.e. nobody uses TC
    
    
        # *** Ajout de stations de TC ***
        #duree du trajet en TC depuis les gares vers le centre, par rapport au
        #trajet equivalent en voiture (doit etre evidemment < 1 pour qu'il y ait un effet,
        #sinon personne ne prend le TC...)
        duree_trajet_TC_vers_centre=0.8
        
        
        # *** station 1 ***
        #coordinates of the station
        xx=0
        yy=15
        #price to go to the center from the station by TC
        prix_TC_ici=prix_VP[(grille.coord_X==xx)&(grille.coord_Y==yy)]*duree_trajet_TC_vers_centre
        prix_TC_ici=prix_TC_ici[0]
        #price to go to the station from any point on the map
        prix_trajet_vers_gare=((grille.coord_X-xx)**2 +
            (grille.coord_Y-yy)**2)**(0.5)*prix_transport_par_km
        #prix_TC c'est le min entre le prix_TC initial et le trajet via la
        #gare
        prix_TC=np.fmin(prix_TC,prix_TC_ici + prix_trajet_vers_gare)
        
        
        # *** station 2 ***
        #coordinates of the station
        xx=0
        yy=30
        #price to go to the center from the station by TC
        prix_TC_ici=prix_VP[(grille.coord_X==xx)&(grille.coord_Y==yy)]*duree_trajet_TC_vers_centre
        prix_TC_ici=prix_TC_ici[0]
        #price to go to the station from any point on the map
        prix_trajet_vers_gare=((grille.coord_X-xx)**2 +
            (grille.coord_Y-yy)**2)**(0.5)*prix_transport_par_km
        #prix_TC c'est le min entre le prix_TC initial et le trajet via la
        #gare
        prix_TC=np.fmin(prix_TC,prix_TC_ici + prix_trajet_vers_gare)
        
        
        # *** station 3 ***
        #coordinates of the station
        xx=0
        yy=40
        #price to go to the center from the station by TC
        prix_TC_ici=prix_VP[(grille.coord_X==xx)&(grille.coord_Y==yy)]*duree_trajet_TC_vers_centre
        prix_TC_ici=prix_TC_ici[0]
        #price to go to the station from any point on the map
        prix_trajet_vers_gare=((grille.coord_X-xx)**2 +
            (grille.coord_Y-yy)**2)**(0.5)*prix_transport_par_km
        #prix_TC c'est le min entre le prix_TC initial et le trajet via la
        #gare
        prix_TC=np.fmin(prix_TC,prix_TC_ici + prix_trajet_vers_gare)
        
        
        tous_prix=np.vstack((prix_VP,prix_TC))#les prix concaténés
        prix_transport=np.amin(tous_prix, axis=0)
        mode=np.argmin(tous_prix, axis=0)
    
        self.prix_transport_par_km=prix_transport_par_km
        self.prix_VP=prix_VP
        self.prix_TC=prix_TC
        self.mode=mode
        self.prix_transport=prix_transport
        
    def create_trans_simple(self,prix_transport_par_km,grille:Grille_simulation):
        
        prix_VP=grille.distance_centre*prix_transport_par_km
    
        prix_TC=float('Inf')*np.ones(len(prix_VP))
        
        tous_prix=np.vstack((prix_VP,prix_TC))#les prix concaténés
        prix_transport=np.amin(tous_prix, axis=0)
        mode=np.argmin(tous_prix, axis=0)
    
        self.prix_transport_par_km=prix_transport_par_km
        self.prix_VP=prix_VP
        self.prix_TC=prix_TC
        self.mode=mode
        self.prix_transport=prix_transport
        
    def create_trans_data(self,prix_VP,prix_TC):
        
        tous_prix=np.vstack((prix_VP,prix_TC))#les prix concaténés
        prix_transport=np.amin(tous_prix, axis=0)
        mode=np.argmin(tous_prix, axis=0)
        
        self.prix_transport_par_km=0
        self.prix_VP=prix_VP
        self.prix_TC=prix_TC
        self.mode=mode
        self.prix_transport=prix_transport
            
            

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""
        return ("Trans:\n  prix_transport_par_km: {}\nprix_VP: {}\nprix_TC: {}\nmode: {}\nprix_transport: {}\n".format(
            self.prix_transport_par_km,self.prix_VP,self.prix_TC,self.mode,self.prix_transport))


class Etat_initial:
    
    def __init__(self,population=0,rent=0,hous=0,mode=0,housing=0,people=0,R_0=0,people_travaille=0):
        self.population=population
        self.rent=rent
        self.hous=hous
        self.housing=housing
        self.people=people
        self.R_0=R_0
        self.people_travaille=people_travaille
        
    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur."""
        return ("Etat_initial:\n  population: {}\n  rent: {}\n  hous: {}\n  housing: {}\n  people: {}\n  R_0:{}\n".format(
            self.population,self.rent,self.hous,self.housing,self.people,self.R_0))

    def compute_ville(self,R_0,param,trans,land):
        beta=param["beta"]
        alpha=1-beta
        revenu=param["revenu"]
        A=param["A"]
        b=param["b"]
        a=1-b
        delta=param["delta"]
    
        # revenu minus transport, or 0 if it is negative
        revenu_minus_transport_positive=np.fmax(
            revenu-trans.prix_transport,np.zeros(len(trans.prix_transport))
            )
        
        rent= (R_0* 
               revenu_minus_transport_positive**(1/beta)
               /revenu**(1/beta)
               )
        
        #pour enlever le warning quand on divise par 0
        np.seterr(divide='ignore', invalid='ignore')
        hous = beta * revenu_minus_transport_positive /rent
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
    
        population=np.sum(people*land.coeff_land)
    
        self.population=population
        self.rent=rent
        self.hous=hous
        self.housing=housing
        self.people=people
        self.R_0=R_0
