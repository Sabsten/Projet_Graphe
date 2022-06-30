from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import random

def get_dist(data, routing, solution):
    """Renvoie la distance totale de la solution"""
    route_dist = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        route_dist.append(route_distance)
    return route_dist

def get_routes(solution, routing, manager):
  """Renvoie la liste des routes de la solution"""
  routes = {}
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
      index = solution.Value(routing.NextVar(index))
      route.append(manager.IndexToNode(index))
    routes[route_nbr + 1] = route
  return routes

def get_load(data, solution, routing, manager):
  """Renvoie la liste des routes de la solution"""
  routes_load = []
  for route_nbr in range(routing.vehicles()):
    index = routing.Start(route_nbr)
    route_load = 0
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        index = solution.Value(routing.NextVar(index))
        route_load += data['demands'][node_index]
    routes_load.append(route_load)
  return routes_load

def ortool_CVRP_method(matrice, nb_vehicule, delivery, camion_capacities):
    """Methode main de l'algorithme"""
    # Instancier le problème
    data = {}
    data['demands'] = delivery
    data['vehicle_capacities'] = camion_capacities
    data['distance_matrix'] = matrice
    data['num_vehicles'] = nb_vehicule
    data['depot'] = 0
    # Création du routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    # Creation du routing model
    routing = pywrapcp.RoutingModel(manager)


    # Creation du callback (distance entre 2 noeuds)
    def distance_callback(from_index, to_index):
        """Renvoie la distance entre 2 noeuds"""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Defini le cout de chaque arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Ajout d'une contrainte de capacité
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
    search_parameters.time_limit.FromSeconds(1)

    solution = routing.SolveWithParameters(search_parameters)

    routes = get_routes(solution, routing, manager)

    load = get_load(data, solution, routing, manager)

    return routes, get_dist(data, routing, solution), load
