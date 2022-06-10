from math import sin, cos, sqrt, atan2, radians
from numpy import arccos
from geopy import distance
import time
import random

nb_iteration = int(input("Nombre d'itérations : "))

capitole = (43.6044499, 1.444494)
cesi = (43.5481937, 1.5025686)
eiffel = (48.8582602,2.2944991)
rio = (-22.9519173, -43.2104585)

R = 6371

duree_geodesic = 0.0
duree_great_circle = 0.0
duree_haversine = 0.0
duree_pythagore = 0.0
duree_sinus = 0.0

# Haversine formula is great-circle
def Haversine(pointA, pointB): 
    latitude1 = radians(float(pointA[0]))
    latitude2 = radians(float(pointB[0]))
    deltaLatitude = radians(float(pointB[0]) - float(pointA[0]))
    deltaLongitude = radians(float(pointA[1]) - float(pointB[1]))
    a = sin(deltaLatitude/2)**2 + cos(latitude1) * cos(latitude2) * sin(deltaLongitude/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def Pythagore(pointA, pointB):
    k = 1.852*60
    x = (pointB[0] - pointA[0])* cos((pointA[1] + pointB[1])/2)
    y = (pointB[1] - pointA[1])
    return sqrt(x**2 + y**2) * k

def Sinus(pointA, pointB):
    a = sin(radians(pointA[1]))*sin(radians(pointB[1])) + cos(radians(pointA[1]))*cos(radians(pointB[1]))*cos(radians(pointB[0]) - radians(pointA[0]))
    return R * arccos(a)

for i in range(nb_iteration):
    
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    pointA = (lat, lon)

    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    pointB = (lat, lon)

    start = time.time()
    distance.geodesic(pointA, pointB).km
    duree_geodesic += time.time() - start

    start = time.time()
    distance.great_circle(pointA, pointB).km
    duree_great_circle += time.time() - start

    start = time.time()
    Haversine(pointA, pointB)
    duree_haversine += time.time() - start

    start = time.time()
    Pythagore(pointA, pointB)
    duree_pythagore += time.time() - start

    start = time.time()
    Sinus(pointA, pointB)
    duree_sinus += time.time() - start

print(f"duree moyenne geodesic : {duree_geodesic} sur {nb_iteration} itérations (moyenne de {duree_geodesic/nb_iteration} par calcul)")
print(f"duree moyenne great-circle : {duree_great_circle} sur {nb_iteration} itérations (moyenne de {duree_great_circle/nb_iteration} par calcul)")
print(f"duree moyenne haversine : {duree_haversine} sur {nb_iteration} itérations (moyenne de {duree_haversine/nb_iteration} par calcul)")
print(f"duree moyenne pythagore : {duree_pythagore} sur {nb_iteration} itérations (moyenne de {duree_pythagore/nb_iteration} par calcul)")
print(f"duree moyenne sinus : {duree_sinus} sur {nb_iteration} itérations (moyenne de {duree_sinus/nb_iteration} par calcul)")
print("------------------------------------------------------")
print(f"distance capitole - cesi avec Geodesic: {distance.geodesic(capitole, cesi)} km")
print(f"distance capitole - cesi avec Great-circle: {distance.great_circle(capitole, cesi)} km")
print(f"distance capitole - cesi avec Haversine: {Haversine(capitole, cesi)} km")
print(f"distance capitole - cesi avec Pythagore: {Pythagore(capitole, cesi)} km")
print(f"distance capitole - cesi avec Sinus: {Sinus(capitole, cesi)} km")
print("------------------------------------------------------")
print(f"distance capitole - tour eiffel avec Geodesic: {distance.geodesic(capitole, eiffel)} km")
print(f"distance capitole - tour eiffel avec Great-circle: {distance.great_circle(capitole, eiffel)} km")
print(f"distance capitole - tour eiffel avec Haversine: {Haversine(capitole, eiffel)} km")
print(f"distance capitole - tour eiffel avec Pythagore: {Pythagore(capitole, eiffel)} km")
print(f"distance capitole - tour eiffel avec Sinus: {Sinus(capitole, eiffel)} km")
print("------------------------------------------------------")
print(f"distance capitole - rio avec Geodesic: {distance.geodesic(capitole, rio)} km")
print(f"distance capitole - rio avec Great-circle: {distance.great_circle(capitole, rio)} km")
print(f"distance capitole - rio avec Haversine: {Haversine(capitole, rio)} km")
print(f"distance capitole - rio avec Pythagore: {Pythagore(capitole, rio)} km")
print(f"distance capitole - rio avec Sinus: {Sinus(capitole, rio)} km")
