import os.path
from random import *
import math

class localisation:
    def __init__(self):
        self.CodePostal = ""
        self.Ville = ""
        self.Latitude = ""
        self.Longitude = ""
        self.code_departement = ""
        self.nom_depart = ""
        self.region = ""
        self.ordre = 0


def readfile(n_departemnt):
    "Lis le fichier LocalisationData.csv et retourne une liste d'objets de localisation"
    CheminData = os.path.abspath(os.path.dirname(__file__)) + '\LocalisationData.csv'
    with open(CheminData, 'r') as LocalisationData:
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

def Mapping(PointsTravail, nombre_livraison):
    "Mappe les points de livraison"
    PointsLivraison = []
    DictonaireLivraison = {}
    for _ in range(nombre_livraison):
        index = randint(0, len(PointsTravail)-1)
        PointsLivraison.append(PointsTravail[index])
        DictonaireLivraison[_] = PointsTravail[index].Ville
    return DictonaireLivraison, PointsLivraison

def CalculDistanceHaversine(PointDepart, PointArrive):
    "Calcule la distance entre deux localisations"
    R = 6371 # Rayon de la terre en km
    latitude1 = math.radians(float(PointDepart.Latitude))
    latitude2 = math.radians(float(PointArrive.Latitude))
    deltaLatitude = math.radians(float(PointArrive.Latitude) - float(PointDepart.Latitude))
    deltaLongitude = math.radians(float(PointArrive.Longitude) - float(PointDepart.Longitude))
    a = math.sin(deltaLatitude/2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(deltaLongitude/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def generateMatrix(num_dept, nb_livraison):
    PointsTravail = readfile(num_dept)
    DictonaireLivraison, PointLivraison = Mapping(PointsTravail, nb_livraison)
    # print(f"Point de départ : {PointLivraison[0].Ville}")
    MatriceDistances = []
    MatriceLocalisation = []
    for i in range(len(PointLivraison)):
        MatriceDistances.append([])
        MatriceLocalisation.append([])
        for j in range(len(PointLivraison)):
            MatriceDistances[i].append(round(CalculDistanceHaversine(PointLivraison[i], PointLivraison[j])))
            MatriceLocalisation[i].append(f"{PointLivraison[i].Ville}->{PointLivraison[j].Ville}")
    return MatriceDistances, PointLivraison

