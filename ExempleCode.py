import networkx as nx
import matplotlib.pyplot as plt
import random 
from string import ascii_lowercase
import numpy as np
import time
import random, operator, pandas as pd
from numpy.random import choice
from IPython.display import clear_output
import math
import datetime
from networkx.algorithms import tournament
from bokeh.models import CustomJS, Slider, Button
from bokeh.layouts import row, column
from bokeh.plotting import show
from bokeh.io import output_notebook
from datetime import timedelta, date
import warnings
warnings.simplefilter('ignore')

class City:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.start_date = random_date(START_DATE, END_DATE)
        self.end_date = random_date(self.start_date, END_DATE)
        self.delivered_date = None
    
    # calculate the time to go to another city in minute
    def time(self, city, currentTime):
        dist = nx.astar_path_length(G, self.key, city.key, None, "distance")
        nodesCrossed = len(nx.astar_path(G, self.key, city.key, None, None))-1
        cityCrossedList = nx.astar_path(G, self.key, city.key, None, None)
        
        lastCity = self.key
        totalTraficAmount = 0
        for i in range (0, len(cityCrossedList) -1):
            for road in roadList:
                if ((road.id_city_1 == cityCrossedList[i]) and (road.id_city_2 == cityCrossedList[i+1])) or ((road.id_city_2 == cityCrossedList[i]) and (road.id_city_1 == cityCrossedList[i+1])):
                    for tr in road.traficList:
                        if tr.date == currentTime:
                            totalTraficAmount = totalTraficAmount + tr.nbr_vehicules
                            break
                            
        trafic_coef = (((totalTraficAmount / nodesCrossed) * 10) / MAX_TRAFIC)
        timeToReturn = (dist * trafic_coef) * COEF_TIME
        return int(timeToReturn) + 1
    
    def availability(self):
        return "(" + self.start_date.strftime("%H:%M") + " => " + self.end_date.strftime("%H:%M") +")"
    
    def __repr__(self):
        return "(City :" + self.name + "; with key: " + str(self.key) + ")"
    
class Route:
    def __init__(self, cityList, path):
        if(cityList == None):
            self.path = path
        else:  
            self.path = self.generatePath(cityList)
        self.currentTime = START_DATE
        self.reportedDelivery = 0
        self.delivered_dates = []
        self.cityBanned = []
    
    def generatePath(self, cityList):
        path = random.sample(cityList, len(cityList))
        return path
    
    def __repr__(self):
        return "(Path :" + str(len(self.path)) + "; Current Time: " + str(self.currentTime.strftime("%Y-%m-%d")) + ")"
             
class Road:
    def __init__(self, key, id_city_1, id_city_2):
        self.key = key
        self.id_city_1 = id_city_1
        self.id_city_2 = id_city_2
        self.trafic = random.randint(MIN_TRAFIC, MAX_TRAFIC)
        self.traficList = self.generateTraficList()
            
    def generateTraficList(self):
        tL = []
        start_date = START_DATE
        end_date = END_DATE
        delta = timedelta(minutes=1)
        while start_date <= end_date:
            nbrCars = random.randint(MIN_TRAFIC,MAX_TRAFIC)
            if (timedelta(hours=7) <= timedelta(hours=start_date.hour) < timedelta(hours=9)) or (timedelta(hours=17) <= timedelta(hours=start_date.hour) < timedelta(hours=19)):
                nbrCars = nbrCars * SCALE_TRAFIC
            trafic = Trafic(self.key,start_date,nbrCars)
            tL.append(trafic)
            start_date += delta
        return tL
        

    def __repr__(self):
        return "(Road :" + str(self.key) + "; City 1 => " + str(self.id_city_1) + "; City 2 => " + str(self.id_city_2) + ")"

class Trafic:
    def __init__(self, id_road, date, nbr_vehicules):
        self.id_road = id_road
        self.date = date
        self.nbr_vehicules = nbr_vehicules

    def __repr__(self):
        return "(Trafic : Road:" + self.id_road + "; Date:" + str(self.date) + "; Nombre de véhicules: " + str(self.nbr_vehicules) + ")"
        
#class to calcul the route distance then the fitness value
class Fitness:
    def __init__(self, route):
        self.route = route
        self.time = 0
        self.fitness = 0.0
    
    def routeTime(self):
        self.route.currentTime = START_DATE
        self.route.reportedDelivery = 0
        self.route.delivered_dates = []
        self.route.cityBanned = []
        
        if self.time == 0:
            pathTime = 0
            # on ajoute le temps pour la 1ere ville partant du dépot
            startCity = depot
            toCity = self.route.path[0]
            timeToGo = startCity.time(toCity,self.route.currentTime)
            arrivedExpected = self.route.currentTime + timedelta(minutes=timeToGo)
            timeToWait = toCity.start_date - arrivedExpected
            deltatime = int(timeToWait.seconds/60) + timeToGo
            self.route.currentTime += timedelta(minutes=deltatime)
            self.route.delivered_dates.append(self.route.currentTime)
            pathTime += deltatime
            
            for i in range(len(self.route.path)):
                deltaTime = 0
                fromCity = self.route.path[i]
                toCity = None
                if i + 1 < len(self.route.path):
                    toCity = self.route.path[i + 1]
                else:
                    toCity = self.route.path[0]

                # on cacul l'heure d'arrviée pour ensuite vérifier si la ville est disponible
                timeToGo = fromCity.time(toCity,self.route.currentTime)
                arrivedExpected = self.route.currentTime + timedelta(minutes=timeToGo)
                
                if(arrivedExpected > toCity.end_date and i + 1 < len(self.route.path)):
                    # colis non délivré => reporté à demain
                    self.route.cityBanned.append(toCity.key)
                    self.route.reportedDelivery += 1
                elif(arrivedExpected < toCity.start_date):
                    # colis délivré avec une attente de timeToWait minute
                    timeToWait = toCity.start_date - arrivedExpected
                    # on ajoute le temps attendus 
                    deltaTime += int(timeToWait.seconds/60) + timeToGo
                else:
                    # colis délivré
                    deltaTime += timeToGo
                
                self.route.currentTime += timedelta(minutes=deltaTime)
                if(deltaTime > 0 and i + 1 < len(self.route.path)):
                    self.route.delivered_dates.append(self.route.currentTime)
                pathTime += deltaTime
            
            # temps réel de livraison
            self.time = pathTime
            
            # temps de livraison avec un ajout de pénalité ppur la prochaine génération
            penalityTime = self.route.reportedDelivery / len(self.route.path) + 1
            
        return self.time * penalityTime
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeTime())
        return self.fitness