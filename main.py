import math as math
import os.path
from random import *
import folium
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
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


def genererCarte(ordre, PointLivraison):
    "Génère une carte"
    Carte = folium.Map(location=[PointLivraison[0].Latitude, PointLivraison[0].Longitude], zoom_start=10)
    i=1
    for each_item in PointLivraison:
        folium.Marker(location=[each_item.Latitude, each_item.Longitude], popup=f"{each_item.Ville}({str(ordre[i])})", icon=folium.Icon(color='green')).add_to(Carte)
        i=i+1
    folium.PolyLine([(float(each_item.Latitude), float(each_item.Longitude)) for each_item in PointLivraison], color='red', weight=1).add_to(Carte)
    Carte.save(os.path.abspath(os.path.dirname(__file__))+ '\Map.html')
    webbrowser.open('file://' + os.path.realpath('Map.html'))

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(1):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))
    return plan_output

def main():
    DepartementTravail = randint(1,93)
    nombre_livraison = 8
    print(f"Departement de travail : {str(DepartementTravail)}")
    PointsTravail = readfile(DepartementTravail)
    MateriauxSpecial = randint(1, len(PointsTravail)-1)
    PointLivraison = Mapping(PointsTravail, nombre_livraison)
    numvehicule = 1
    print(f"Point de départ : {PointLivraison[0].Ville}")
    MatriceDistances, MatriceLocalisation = GenererMatrice(PointLivraison)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(MatriceDistances),numvehicule, 0)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return MatriceDistances[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(MatriceDistances, manager, routing, solution)
    else:
        print('No solution found !')

    #GenerateMap
    genererCarte(str(print_solution(MatriceDistances, manager, routing, solution)).split(" -> "),PointLivraison)


main()
