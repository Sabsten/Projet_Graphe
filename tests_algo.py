from Algorithms.or_tools import ortools_method
from Algorithms.vrpy import vrpy_methode
from generateMatrix import generateMatrix
from genererCarte import genererCarte
from random import *

# ortools_method()

def main():
    DepartementTravail = randint(1,93)
    nombre_livraison = int(input("Nombre de livraison : "))
    matriceDistance, pointsLivraison = generateMatrix(DepartementTravail, nombre_livraison)
    # print(matriceDistance)
    nb_vehicule = int(input("Nombre de vehicule : "))
    bestRoute = ortools_method(matriceDistance, nb_vehicule)
    vrpy_methode(matriceDistance, pointsLivraison, nb_vehicule)
    # genererCarte(bestRoute, pointsLivraison)

if __name__ == "__main__":
    main()
