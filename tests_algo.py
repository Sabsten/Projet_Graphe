from Algorithms.or_tools import ortools_method
from Algorithms.vrpy import vrpy_methode
from Algorithms.tabu import tabu_method
from Algorithms.genetic import genetic_method
from Algorithms.antColony import antColony_method
from generateMatrix import generateMatrix
from genererCarte import genererCarte

from random import *

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

    ortools_route = ortools_method(matriceDistance, nb_vehicule)
    tabu_route, tabu_dist = tabu_method(matriceDistance, nb_vehicule, maxIteration)
    genetic_route, genetic_dist = genetic_method(mutationRate, populationSize, maxGen, maxIteration, nb_vehicule, matriceDistance)
    ant_route, ant_dist = antColony_method(matriceDistance, nb_vehicule)
    vrpy_route, vrpy_cost = vrpy_methode(matriceDistance, pointsLivraison, nb_vehicule)

    print("\n")
    print("### VRPY ###")
    vrpy_globalDist = 0
    for i in range(len(vrpy_route)):
        print(f"route : {vrpy_route[i+1]} || cost = {vrpy_cost[i+1]} km")
        vrpy_globalDist += vrpy_cost[i+1]
    print(f"Global distance : {vrpy_globalDist} km")
    print("\n")

    print(f"### TABU ###")
    tabu_globalDist = 0
    for i in range(len(tabu_route)):
        print(f"route : {tabu_route[i+1]} || cost = {tabu_dist[i]} km")
        tabu_globalDist += tabu_dist[i]
    print(f"Total distance = {tabu_globalDist} km")
    print("\n")

    print(f"### GENETIC ###")
    genetic_globalDist = 0
    for i in range(len(genetic_route)):
        print(f"route : {genetic_route[i+1]} || cost = {genetic_dist[i]} km")
        genetic_globalDist += genetic_dist[i]
    print(f"Total distance = {genetic_globalDist} km")
    print("\n")

    print(f"### ANT COLONY ###")
    ant_globalDist = 0
    for i in range(len(ant_route)):
        print(f"route : {ant_route[i+1]} || cost = {ant_dist[i]} km")
        ant_globalDist += ant_dist[i]
    print(f"Total distance = {ant_globalDist} km")


    # genererCarte(ortools_route, pointsLivraison, "ortools")
    # genererCarte(vrpy_route, pointsLivraison, "vrpy")
    # genererCarte(tabu_route, pointsLivraison, "tabu")
    # genererCarte(genetic_route, pointsLivraison, "genetic")
    # genererCarte(ant_route, pointsLivraison, "antColony")

if __name__ == "__main__":
    main()
