from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from vrpy import VehicleRoutingProblem
from numpy import array

def vrpy_methode(Matrice, pointsLivraison, nb_vehicule):
    # Modify the distance matrix to make it compatible with the VRPY algorithm.
    for i in range(len(pointsLivraison)):
        Matrice[i].insert(0, 0)
    Matrice.append([0 for _ in range(len(pointsLivraison)+1)])

    # Create the graph.
    A = array(Matrice, dtype=[("cost", float)])
    G = from_numpy_matrix(A, create_using=DiGraph())

    # The depot is relabeled as Source and Sink
    G = relabel_nodes(G, {0: "Source", len(G)-1: "Sink"})

    prob = VehicleRoutingProblem(G)
    # prob.minimize_global_span = True
    prob.num_vehicles = nb_vehicule
    prob.use_all_vehicles = True
    prob.solve()
    return prob.best_routes, prob.best_routes_cost