from Algorithms.or_tools import ortools_method
from Algorithms.vrpy import vrpy_methode
from Algorithms.tabu import tabu
from generateMatrix import generateMatrix
from genererCarte import genererCarte

from random import *

def main():
    DepartementTravail = randint(1,93)
    nombre_livraison = int(input("Nombre de livraison : "))
    matriceDistance, pointsLivraison = generateMatrix(DepartementTravail, nombre_livraison)
    # print(matriceDistance)
    nb_vehicule = int(input("Nombre de vehicule : "))
    ortools_route = ortools_method(matriceDistance, nb_vehicule)
    vrpy_route, vrpy_cost = vrpy_methode(matriceDistance, pointsLivraison, nb_vehicule)
    tabu_bestPath, tabu_bestDist, tabu_lens = tabu(matriceDistance, nb_vehicule, 5)
    print("### VRPY ###")
    for i in range(len(vrpy_route)):
        print("\r")
        print(f"route : {vrpy_route[i+1]} || cost = {vrpy_cost[i+1]} km")
    genererCarte(ortools_route, pointsLivraison, "ortools")
    genererCarte(vrpy_route, pointsLivraison, "vrpy")
    # genererCarte(tabu_route, pointsLivraison, "tabu")

if __name__ == "__main__":
    main()
