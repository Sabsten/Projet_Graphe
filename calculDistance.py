from math import sin, cos, sqrt, atan2, radians
from geopy import distance
import time
import random

nb_iteration = int(input("Nombre d'itérations : "))

duree_geodesic = 0.0
duree_great_circle = 0.0
duree_haversine = 0.0
# Haversine formula is great-circle
def Haversine(pointA, pointB): 
   
    R = 6371
    latitude1 = radians(float(pointA[0]))
    latitude2 = radians(float(pointB[0]))
    deltaLatitude = radians(float(pointB[0]) - float(pointA[0]))
    deltaLongitude = radians(float(pointA[1]) - float(pointB[1]))
    a = sin(deltaLatitude/2)**2 + cos(latitude1) * cos(latitude2) * sin(deltaLongitude/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

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

print(f"duree moyenne geodesic : {duree_geodesic} sur {nb_iteration} itérations (moyenne de {duree_geodesic/nb_iteration} par calcul)")
print(f"duree moyenne great-circle : {duree_great_circle} sur {nb_iteration} itérations (moyenne de {duree_great_circle/nb_iteration} par calcul)")
print(f"duree moyenne haversine : {duree_haversine} sur {nb_iteration} itérations (moyenne de {duree_haversine/nb_iteration} par calcul)")

