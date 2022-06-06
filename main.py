import math as math
import os.path
from random import *
import folium
import matplotlib.pyplot as plt
import webbrowser

class localisation:
    def __init__(self):
        self.CodePostal = ""
        self.Ville = ""
        self.Latitude = ""
        self.Longitude = ""
        self.code_departement = ""
        self.nom_depart = ""
        self.region = ""
        self.numero = 0


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


def GenererMatrice(PointTravail):
    "Génère la matrice des distances"
    MatriceDistances = []
    MatriceLocalisation = []
    for i in range(len(PointTravail)):
        MatriceDistances.append([])
        MatriceLocalisation.append([])
        for j in range(len(PointTravail)):
            MatriceDistances[i].append(CalculDistanceHaversine(PointTravail[i], PointTravail[j]))
            MatriceLocalisation[i].append(PointTravail[j].Ville)
    return MatriceDistances, MatriceLocalisation


def Mapping(PointsTravail, nombre_livraison):
    "Mappe les points de livraison"
    PointsLivraison = []
    Points = PointsTravail
    for _ in range(nombre_livraison):
        index = randint(0, len(Points)-1)
        PointsLivraison.append(Points[index])
        Points.remove(Points[index])
    return PointsLivraison

def TrouverLeCycleLePlusCourt(Matrice):
    distance_min = 10000000000
    cycle_min = []
    for line in range(len(Matrice)):
        if sum(Matrice[line]) < distance_min:
            distance_min = sum(Matrice[line])
            cycle_min = line
    return distance_min, cycle_min

def genererCarte(PointLivraison):
    "Génère une carte"
    Carte = folium.Map(location=[PointLivraison[0].Latitude, PointLivraison[0].Longitude], zoom_start=10)
    i=1
    for each_item in PointLivraison:
        folium.Marker(location=[each_item.Latitude, each_item.Longitude], popup=f"{each_item.Ville}({str(i)})", icon=folium.Icon(color='green')).add_to(Carte)
        i=i+1
    folium.PolyLine([(float(each_item.Latitude), float(each_item.Longitude)) for each_item in PointLivraison], color='red', weight=1).add_to(Carte)
    Carte.save(os.path.abspath(os.path.dirname(__file__))+ '\Map.html')
    webbrowser.open('file://' + os.path.realpath('Map.html'))

def PositionnerPointSurUneCarte(nombre_livraison):
    "Positionne les points sur une carte"
    DepartementTravail = randint(1,93)
    print(f"Departement de travail : {str(DepartementTravail)}")
    PointsTravail = readfile(DepartementTravail)
    MateriauxSpecial = randint(1, len(PointsTravail)-1)
    PointLivraison = Mapping(PointsTravail, nombre_livraison)
    print(f"Point de départ : {PointLivraison[0].Ville}")
    MatriceDistances, MatriceLocalisation = GenererMatrice(PointLivraison)
    print(MatriceLocalisation)
    print(MatriceDistances)
    _, Cycle = TrouverLeCycleLePlusCourt(MatriceDistances)
    print("### ###")
    print("Le cycle de plus petite distance est: ")
    print(MatriceLocalisation[Cycle])
    genererCarte(PointLivraison)

nombre_livraison = 8
PositionnerPointSurUneCarte(nombre_livraison)