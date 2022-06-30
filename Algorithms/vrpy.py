from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from vrpy import VehicleRoutingProblem
from numpy import array

def vrpy_methode(Matrice, pointsLivraison, nb_vehicule):
    # Modifier la matrice pour quelle soit compatible avec VRPY
    for i in range(len(pointsLivraison)):
        Matrice[i].insert(0, 0)
    Matrice.append([0 for _ in range(len(pointsLivraison)+1)])

    # Creation du graphe
    A = array(Matrice, dtype=[("cost", int)])
    G = from_numpy_matrix(A, create_using=DiGraph())

    # Le point de départ et d'arrivée est renommé Source et Sink
    G = relabel_nodes(G, {0: "Source", len(G)-1: "Sink"})

    prob = VehicleRoutingProblem(G)
    # prob.minimize_global_span = True
    prob.num_vehicles = nb_vehicule
    prob.use_all_vehicles = True
    prob.solve()

    routeDist = []
    for i in range(len(prob.best_routes_cost)):
        routeDist.append(prob.best_routes_cost[i+1])
    return prob.best_routes, routeDist