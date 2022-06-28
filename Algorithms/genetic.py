import random

#Classe ADN de trajet
# - Objet décrivant un élément contenu dans la liste population
# - Possède toutes les attributs et méthodes nécessaire à la situation(score de fitness) d'un  élément dans la population
class ADNtrajet:
    
    ADN = list()                #Liste descriptive du trajet ou configuration de trajet totale
    ADNSize = 0               #Taille de la liste ADN
    fitness = 0
    globalFitness = 0
    fitnessList = list()
    vehicleADNlist = list()
    
    
    def __init__(self, values, graph):
        self.ADN = values
        self.ADNSize = len(values)
        self.calcFitness(graph)
        
    def calcFitness(self, graph):
        startPos = 0
        stopPos = 0
        self.fitnessList = list()
        self.vehicleADNlist = list()
        currentVehicleFitness = 0
        for i in range(self.ADNSize-1):
            currentVehicleFitness += graph[self.ADN[i]][self.ADN[i+1]]
            if self.ADN[i+1] == self.ADN[0]:
                stopPos = i+2
                self.vehicleADNlist.append(self.ADN[startPos:stopPos])
                startPos = i+1
                self.fitnessList.append(currentVehicleFitness)
                currentVehicleFitness = 0
        self.fitness = max(self.fitnessList)
        
    def calcGlobalFitness(self, graph):
        # Calcul retour au sommet de départ
        self.globalFitness = 0
        for i in range(self.ADNSize-1):
            self.globalFitness += graph[self.ADN[i]][self.ADN[i+1]]
        
    def forceMutate(self, nbMutation, graph):
        for _ in range(nbMutation):
            swapPos1 = 0
            swapPos2 = 0
            swapDone = True
            while swapDone:
                swapPos1 =  random.randint(1, self.ADNSize-2)
                swapPos2 =  random.randint(1, self.ADNSize-2)
                if swapPos1 != swapPos2:
                    self.ADN[swapPos1], self.ADN[swapPos2] = self.ADN[swapPos2], self.ADN[swapPos1]
                    swapDone = False
        self.calcFitness(graph)
        self.calcGlobalFitness(graph)
                

#END CLASS "ANDtrajet"

import copy

# Population object

class Population:
    
    populations = []
    
    nbMutation = 0.01
    populationSize = 100
    
    graph = []
    nbNode = 0
    nbVehicle = 1
    startPosition = 0
    
    bestPath = list()
    bestFitness = 0
    bestFitnessList = list()
    bestvehiclePath = list()
    bestGlobalFitness = 0
    
    def __init__(self, mutation, size, vehicle, graph, startPos):

        self.nbMutation = mutation
        self.populationSize = size
        self.populations = []*(size + vehicle - 1)
        
        self.graph = graph
        self.nbNode = len(graph)

        if self.nbNode == 0 or self.nbNode == 1:
            print("Error: graph node number is null or unique")
            return

        self.nbVehicle = vehicle
        if 0 <= startPos <= self.nbNode - 1:
            self.startPosition = startPos
        else:
            print("Error: start position not valid, using 0 instead")
            self.startPosition = 0
        
        defaultPath = list()
        for i in range(self.nbNode):
            if i == self.startPosition:
                continue
            defaultPath.append(i)
        for _ in range(self.nbVehicle-1):
            defaultPath.append(self.startPosition)
        
        for i in range(size):
            randomPath = defaultPath.copy()
            random.shuffle(randomPath)
            randomPath.insert(0,self.startPosition)
            randomPath.append(self.startPosition)
            #print(randomPath)
            self.populations.append(ADNtrajet(randomPath, graph))
            
        self.populations.sort(key=lambda x: x.fitness)
        self.bestPath = self.populations[0].ADN.copy()
        self.bestFitness = self.populations[0].fitness
        self.bestFitnessList = self.populations[0].fitnessList
        self.bestvehiclePath = self.populations[0].vehicleADNlist
        self.bestGlobalFitness = self.populations[0].globalFitness
        
    def getPopADNs(self):

        ADNs = list()
        for o in self.populations:
            ADNs.append(o.ADN)
        return ADNs
    
    def isDuplicate(self, i):

        ADNlist = self.getPopADNs()
        ADNlist.pop(i)
        if self.populations[i].ADN in ADNlist:
            # print("EXISTING !")
            return True
        else:
            # print("NOT EXISTING !")
            return False
    
    def printPop(self):
        for o in self.populations:
            print(o.ADN, o.fitness)

    def start(self, maxGen):

        if self.nbNode == 2:
            self.bestPath = [0,1,0]
            self.bestFitness = (self.graph[0][2] * 2)
            return

        checkSmallSize = (self.nbNode**2 - self.nbNode) / 2

        if checkSmallSize <= self.populationSize:
            self.populationSize = round(checkSmallSize) - 1
            self.populations = self.populations[0:self.populationSize]
            maxGen = self.populationSize + 10
        
        for nbGen in range(maxGen):
            for i in range(round(self.populationSize/2)-1):
                self.populations[i+round(self.populationSize/2)] = copy.deepcopy(self.populations[i])
            for i in range(round(self.populationSize/2), self.populationSize):
                self.populations[i].forceMutate(self.nbMutation, self.graph)
                while self.isDuplicate(i):
                    self.populations[i].forceMutate(self.nbMutation, self.graph)
            self.populations.sort(key=lambda x: x.fitness)
            
            
            self.bestPath = self.populations[0].ADN.copy()
            self.bestFitness = self.populations[0].fitness
            self.bestFitnessList = self.populations[0].fitnessList
            self.bestvehiclePath = self.populations[0].vehicleADNlist
            self.bestGlobalFitness = self.populations[0].globalFitness

# Fin de la classe "Population"

# Algo génétique pour solution problème voyageur de commerce complet :
def genetic_method(mut, size, mxGen, mxIte, nbVeh, grph):
    pos = 0
    bestPath = list()
    bestFitnessList = list()
    bestvehiclePath = list()
    bestFitness = 0
    bestGlobalFitness = 0
    for nbIte in range(mxIte):
        pop = Population(mut, size, nbVeh, grph, pos)
        pop.start(mxGen)
        if pop.bestFitness > bestFitness:
            bestPath = pop.bestPath
            bestFitness = pop.bestFitness
            bestFitnessList = pop.bestFitnessList
            bestvehiclePath = pop.bestvehiclePath
            bestGlobalFitness = pop.bestGlobalFitness
    
    route = {i+1:bestvehiclePath[i] for i in range(len(bestvehiclePath))}

    return route, bestFitnessList
    