from Algorithms.or_tools import ortools_method
from Algorithms.vrpy import vrpy_methode
from Algorithms.tabu import tabu_method
from Algorithms.genetic import genetic_method
from Algorithms.antColony import antColony_method
from generateMatrix import generateMatrix
from generateMaps import generateMaps

from random import *

def printer(algo, route, dist):
    """ Affiche les résultats d'un algorithme """
    print(f"### {algo} ###")
    globalDist = 0
    for i in range(len(route)):
        print(f"route : {route[i+1]} || distance = {dist[i]} km")
        globalDist += dist[i]
    print(f"Total distance = {globalDist} km")
    print("\n")
    

def main():

    # Demande du nombre de livraison et du nombre de véhicules
    DepartementTravail = randint(1,93)
    nombre_livraison = int(input("Nombre de livraisons : "))
    matriceDistance, pointsLivraison = generateMatrix(DepartementTravail, nombre_livraison)
    nb_vehicule = int(input("Nombre de vehicules : "))
    print("\n")

    # Paramétrage des algorithmes
    mutationRate = 1
    populationSize = 40
    maxGen = 10000
    maxIteration = 1
    time_limit = 3

    ortools_tabu_route, ortools_tabu_dist = ortools_method(matriceDistance, nb_vehicule, "tabu", time_limit)
    printer("or_tools_tabu", ortools_tabu_route, ortools_tabu_dist)

    ortools_sa_route, ortools_sa_dist = ortools_method(matriceDistance, nb_vehicule, "simulated_annealing", time_limit)
    printer("or_tools_sa", ortools_sa_route, ortools_sa_dist)

    tabu_route, tabu_dist = tabu_method(matriceDistance, nb_vehicule, maxIteration)
    printer("tabu", tabu_route, tabu_dist)

    genetic_route, genetic_dist = genetic_method(mutationRate, populationSize, maxGen, maxIteration, nb_vehicule, matriceDistance)
    printer("genetic", genetic_route, genetic_dist)

    ant_route, ant_dist = antColony_method(matriceDistance, nb_vehicule)
    printer("antColony", ant_route, ant_dist)
    
    # vrpy_route, vrpy_cost = vrpy_methode(matriceDistance, pointsLivraison, nb_vehicule)
    # printer("vrpy", vrpy_route, vrpy_cost)

    # generateMaps(ortools_tabu_route, pointsLivraison, "ortools_tabu")
    # generateMaps(ortools_sa_route, pointsLivraison, "ortools_sa")
    # generateMaps(vrpy_route, pointsLivraison, "vrpy")
    # generateMaps(tabu_route, pointsLivraison, "tabu")
    # generateMaps(genetic_route, pointsLivraison, "genetic")
    # generateMaps(ant_route, pointsLivraison, "antColony")

if __name__ == "__main__":
    main()
