import math as math
from random import *

class localisation:
    def __init__(self):
        self.CodePostal = ""
        self.Ville = ""
        self.Latitude = ""
        self.Longitude = ""
        self.code_departement = ""
        self.nom_depart = ""
        self.region = ""


def readfile(n_departemnt):
    "Lis le fichier LocalisationData.csv et retourne une liste d'objets de localisation"
    with open('C:\\Users\\sebcz\Desktop\Projet_Graphe\LocalisationData.csv', 'r') as LocalisationData:
        Localisation = []
        for line in LocalisationData:
            InfoLine = line.split(';')
            if InfoLine[6] == str(n_departemnt):
                localisationItem = localisation()
                localisationItem.CodePostal = InfoLine[0]
                localisationItem.Ville = InfoLine[1]
                localisationItem.Latitude = InfoLine[2]
                localisationItem.Longitude = InfoLine[3]
                localisationItem.code_departement = InfoLine[6]
                localisationItem.nom_depart = InfoLine[7]
                localisationItem.region = InfoLine[8]
                Localisation.append(localisationItem)
    return Localisation

def CalculDistanceHaversine(PointDepart, PointArrive):
    "Calcule la distance entre deux localisations, a developper avec methode des sin et pythagore"
    R = 6371e3
    latitude1 = math.radians(float(PointDepart.Latitude))
    latitude2 = math.radians(float(PointArrive.Latitude))
    deltaLatitude = math.radians(float(PointArrive.Latitude) - float(PointDepart.Latitude))
    deltaLongitude = math.radians(float(PointArrive.Longitude) - float(PointDepart.Longitude))
    a = math.sin(deltaLatitude/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(deltaLongitude/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def Main():
    DepartementTravail = randint(1,93)
    nombre_vehicule = 1
    nombre_livraison = 4
    print("Le departement de travail est le departement numero: ", DepartementTravail)
    PointsTravail = readfile(DepartementTravail)
    PointLivraison = Mapping(PointsTravail, nombre_livraison)
    Matrice = MatriceDistances(PointLivraison)
    Cycle = TrouverCycleVehiculeRoutingProblem(Matrice)
    print("Le cycle de plus petite distance est: ")
    print(Cycle)

def MatriceDistances(PointTravail):
    "Cree une matrice de distances entre les points de travail"
    MatriceDistances = []
    for depart in range(len(PointTravail)):
        MatriceDistances.append([])
        for arrive in range(len(PointTravail)):
            MatriceDistances[depart].append(round(CalculDistanceHaversine(PointTravail[depart], PointTravail[arrive])/1000))
    return MatriceDistances

def Mapping(PointsTravail, nombre_livraison):
    "Cree une liste de points de livraison"
    PointLivraison = []
    for i in range(nombre_livraison):
        PointLivraison.append(PointsTravail[randint(0, len(PointsTravail)-1)])
    return PointLivraison


def TrouverCycleVehiculeRoutingProblem(MatriceDistances):
    "Cree un cycle de plus petite distance pour un vehicule routing problem"
    Cycle = []
    for depart in range(len(MatriceDistances)):
        Cycle.append(depart)
        for arrive in range(len(MatriceDistances)):
            if arrive != depart and MatriceDistances[depart][arrive] < MatriceDistances[depart][Cycle[0]]:
                Cycle[0] = arrive
    return Cycle
    
Main()
