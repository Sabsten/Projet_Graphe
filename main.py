import math as math
import os.path
from random import *
import folium
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from vrpy import VehicleRoutingProblem
from numpy import array
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
        MatriceDistances.append([0])
        MatriceLocalisation.append([])
        for j in range(len(PointTravail)):
            MatriceDistances[i].append(CalculDistanceHaversine(PointTravail[i], PointTravail[j]))
            MatriceLocalisation[i].append(f"{PointTravail[i].Ville}->{PointTravail[j].Ville}")
    MatriceDistances.append([0 for _ in range(len(PointTravail)+1)])
    return MatriceDistances, MatriceLocalisation


def Mapping(PointsTravail, nombre_livraison):
    "Mappe les points de livraison"
    PointsLivraison = []
    DictonaireLivraison = {}
    for _ in range(nombre_livraison):
        index = randint(0, len(PointsTravail)-1)
        PointsLivraison.append(PointsTravail[index])
        DictonaireLivraison[_] = PointsTravail[index].Ville
    return DictonaireLivraison, PointsLivraison


def genererCarte(ordrepasage, PointLivraison):
    "Génère une carte"
    #Permet de génerer une carte
    Carte = folium.Map(location=[PointLivraison[0].Latitude, PointLivraison[0].Longitude], zoom_start=10)
    i=1
    for each_item in PointLivraison:
        folium.Marker(location=[each_item.Latitude, each_item.Longitude], popup=f"{each_item.Ville}", icon=folium.Icon(color='green')).add_to(Carte)
        each_item.ordre = i-1
        i=i+1

    for each_item in ordrepasage:
        for indice in range(len(ordrepasage[each_item])):
            if type(ordrepasage[each_item][indice]) == str:
                ordrepasage[each_item][indice] = 0

    ListColor = ['red', 'blue', 'green', 'grey', 'orange', 'purple', 'pink', 'brown', 'black', 'grey']
    for indice in ordrepasage:
        folium.PolyLine([(float(PointLivraison[each_item].Latitude), float(PointLivraison[each_item].Longitude)) for each_item in ordrepasage[indice]], color=ListColor[indice], weight=2).add_to(Carte)

    

    Carte.save(os.path.abspath(os.path.dirname(__file__))+ '\Map.html')
    webbrowser.open('file://' + os.path.realpath('Map.html'))


def main():
    DepartementTravail = randint(1,93)
    nombre_livraison = 25
    print(f"Departement de travail : {str(DepartementTravail)}")
    PointsTravail = readfile(DepartementTravail)
    MateriauxSpecial = randint(1, len(PointsTravail)-1)
    DictonaireLivraison, PointLivraison = Mapping(PointsTravail, nombre_livraison)
    print(f"Point de départ : {PointLivraison[0].Ville}")
    MatriceDistances, MatriceLocalisation = GenererMatrice(PointLivraison)
    A = array(MatriceDistances, dtype=[("cost", float)])
    G = from_numpy_matrix(A, create_using=DiGraph())

    # The depot is relabeled as Source and Sink
    G = relabel_nodes(G, {0: "Source", len(G)-1: "Sink"})

    prob = VehicleRoutingProblem(G)
    prob.minimize_global_span = True
    prob.solve()
    print(prob.best_routes)
    genererCarte(prob.best_routes,PointLivraison)


main()
