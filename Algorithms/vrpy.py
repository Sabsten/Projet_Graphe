from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from vrpy import VehicleRoutingProblem
from numpy import array

def vrpy_methode(Matrice, pointsLivraison, nb_vehicule):
    for i in range(len(pointsLivraison)):
        Matrice[i].insert(0, 0)
    Matrice.append([0 for _ in range(len(pointsLivraison)+1)])
    A = array(Matrice, dtype=[("cost", float)])
    G = from_numpy_matrix(A, create_using=DiGraph())

    # The depot is relabeled as Source and Sink
    G = relabel_nodes(G, {0: "Source", len(G)-1: "Sink"})

    print(G.nodes())
    prob = VehicleRoutingProblem(G)
    prob.minimize_global_span = True
    prob.num_vehicles = nb_vehicule
    prob.solve()
    print(prob.best_routes)