from Algorithms.or_tools import ortools_method
from Algorithms.vrpy import vrpy_methode
from Algorithms.tabu import tabu_method
from Algorithms.genetic import genetic_method
from Algorithms.antColony import antColony_method
from generateMatrix import generateMatrix
from genererCarte import genererCarte

from random import *

def printer(algo, route, dist):
    print(f"### {algo} ###")
    globalDist = 0
    for i in range(len(route)):
        print(f"route : {route[i+1]} || distance = {dist[i]} km")
        globalDist += dist[i]
    print(f"Total distance = {globalDist} km")
    print("\n")
    

def main():
    DepartementTravail = randint(1,93)
    nombre_livraison = int(input("Nombre de livraison : "))
    matriceDistance, pointsLivraison = generateMatrix(DepartementTravail, nombre_livraison)
    nb_vehicule = int(input("Nombre de vehicule : "))
    print("\n")

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
    
    vrpy_route, vrpy_cost = vrpy_methode(matriceDistance, pointsLivraison, nb_vehicule)
    printer("vrpy", vrpy_route, vrpy_cost)

    genererCarte(ortools_tabu_route, pointsLivraison, "ortools_tabu")
    genererCarte(ortools_sa_route, pointsLivraison, "ortools_sa")
    genererCarte(vrpy_route, pointsLivraison, "vrpy")
    genererCarte(tabu_route, pointsLivraison, "tabu")
    genererCarte(genetic_route, pointsLivraison, "genetic")
    genererCarte(ant_route, pointsLivraison, "antColony")

if __name__ == "__main__":
    main()
