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
        MatriceDistances.append([])
        MatriceLocalisation.append([])
        for j in range(len(PointTravail)):
            MatriceDistances[i].append(CalculDistanceHaversine(PointTravail[i], PointTravail[j]))
            MatriceLocalisation[i].append(f"{PointTravail[i].Ville}->{PointTravail[j].Ville}")

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

def TrouverLeCycleLePlusCourt(PointLivraison, MatriceDistance,MatriceLocalisation,point_depart):
    ListeParcours = []
    ListeDistances = []
    distancemax = 10000000000
    intersection = point_depart
    cycle,j  = 0,0
    ordre = 1
    trajetsupprime = 0
    while len(MatriceDistance) != 0:
        if MatriceDistance[0] == []:
            return ListeParcours,ListeDistances
        if MatriceLocalisation[cycle][0].split('->')[0] == intersection:
            PointLivraison[cycle].ordre = ordre
            while j != len(MatriceDistance) - trajetsupprime:
                if MatriceDistance[cycle][j] < distancemax and MatriceDistance[cycle][j] != 0:
                    distancemax = MatriceDistance[cycle][j]
                    trajet = MatriceLocalisation[cycle][j]
                    indice = j
                j += 1
            ListeParcours.append(trajet)
            ListeDistances.append(distancemax)
            for cycle in range(len(MatriceDistance)):
                MatriceDistance[cycle].pop(indice)
                MatriceDistance[cycle].remove
                MatriceLocalisation[cycle].pop(indice)
                MatriceLocalisation[cycle].remove
            intersection = trajet.split('->')[1]
            distancemax = 10000000000
            trajetsupprime = trajetsupprime +1
            ordre = ordre + 1
            cycle = 0
            j=0
        else:
            cycle = cycle + 1
        

def genererCarte(PointLivraison):
    "Génère une carte"
    Carte = folium.Map(location=[PointLivraison[0].Latitude, PointLivraison[0].Longitude], zoom_start=10)
    i=1
    PointLivraison.sort(key=lambda x: x.ordre)
    for each_item in PointLivraison:
        folium.Marker(location=[each_item.Latitude, each_item.Longitude], popup=f"{each_item.Ville}({str(each_item.ordre)})", icon=folium.Icon(color='green')).add_to(Carte)
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
    Cycle, ListeDistances = TrouverLeCycleLePlusCourt(PointLivraison, MatriceDistances,MatriceLocalisation, MatriceLocalisation[0][0].split('->')[0])
    print("### ###")
    print("Le cycle de plus petite distance est: ")
    print(Cycle)
    genererCarte(PointLivraison)

nombre_livraison = 8
PositionnerPointSurUneCarte(nombre_livraison)
