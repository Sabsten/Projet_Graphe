def calcPathEfficiency(graph, paths, doPrint = True):
    nbVehicules = len(paths)
    size = len(graph)
    
    totLen = 0
    totLenVehicules = [0 for i in range(nbVehicules)]
    
    # Verifie le chemin pour chaque vehicule
    prefix = "[INVALID PATH]"
    for v in range(nbVehicules):
        if(paths[v][0] != paths[v][len(paths[v])-1]):
            print(prefix, "Path for vehicule", v, "does not return to starting point!")
    concatPaths = [j for i in paths for j in i]
    for i in range(size):
        if(i not in concatPaths):
            print(prefix, "The point", i, "is not taken by any vehicule!")
    if(len(concatPaths) > size + (len(paths)*2)-1):
        print(prefix, "Invalid path length! (Some points are taken multiple times?)")
        print("> Got", len(concatPaths), "expected", size + (len(paths)*2)-1)
    
    # Calcul de la distance du chemin
    for v in range(nbVehicules):
        for i in range(len(paths[v])):
            if(i+1 >= len(paths[v])):
                break
            current = paths[v][i]
            neighbour = paths[v][i+1]
            weight = graph[current][neighbour]
            totLen += weight
            totLenVehicules[v] += weight
    
    if(doPrint):
        print("Total weight:", totLen)
    if(doPrint):
        for i in range(nbVehicules): print(" - Weight for vehicule", i, ":", totLenVehicules[i])
    worst = max(totLenVehicules)
    worstIndex = totLenVehicules.index(worst)
    if(doPrint):
        print("Worst weight found for vehicule", worstIndex, "(", worst, ")")
    
    return (worst, worstIndex, totLenVehicules)

def tabu_method(graph, nbVehicules, nbIter, startPoint = 0, concat = False):
    """ Methode main de l'algorithme tabu """
    initGraph = graph
    startPoint = 0
    
    # Initialisation de la liste tabou (stocke un chemin entre deux points)
    tabuList = [[] for i in range(nbVehicules)]
    maxTabuListSize = 50
    
    bestPathIteration = {}
    
    for it in range(nbIter):
        
        currentElements = [startPoint] * nbVehicules
        bestPaths = [[startPoint] for i in range(nbVehicules)]
        bestDistances = [[] for i in range(nbVehicules)]
        visited = [startPoint]
        
        totLens = [0] * nbVehicules
        totPoints = len(graph)
        
        prematurateEnd = False

        while len(visited) < len(graph) and not prematurateEnd:

            # Boucle sur les vehicules
            for v in range(nbVehicules):

                if(len(visited) >= len(graph)):
                    break

                # Pire cas
                bestDistance = 99999999999
                bestNeighbour = startPoint

                # Trouver le voisin le plus proche
                for j in range(totPoints):
                    # Si le point n'a pas encore été visité
                    if(currentElements[v] != j and j not in visited and (currentElements[v], j) not in tabuList[v]):
                        neighbour = graph[currentElements[v]][j]
                        if(neighbour <= bestDistance):
                            bestDistance = neighbour
                            bestNeighbour = j
                            tabuList[v].append((currentElements[v], j))
                            if(len(tabuList[v]) > maxTabuListSize):
                                tabuList[v].pop(0)

                # Impossible de trouver une solution
                if(bestNeighbour == startPoint):
                    # Recherche meilleur voisin
                    for j in range(totPoints):
                        # Si le point n'a pas encore été visité
                        if(currentElements[v] != j and j not in visited):
                            neighbour = graph[currentElements[v]][j]
                            if(neighbour <= bestDistance):
                                bestDistance = neighbour
                                bestNeighbour = j
                
                bestPaths[v].append(bestNeighbour)
                visited.append(bestNeighbour)
                currentElements[v] = bestNeighbour
                totLens[v] += bestDistance
                bestDistances[v].append(bestDistance)

        for v in range(nbVehicules):
            bestPaths[v].append(startPoint)
            totLens[v] += graph[currentElements[v]][startPoint]
            bestDistances[v].append(graph[currentElements[v]][startPoint])
            
        worst, worstIndex, tot = calcPathEfficiency(initGraph, bestPaths, False)

        if bestPathIteration.get("worst") is None or worst < bestPathIteration["worst"]:
            bestPathIteration = {
                "bestPaths": bestPaths,
                "bestDistances": bestDistances,
                "totLens": totLens,
                "worst": worst
            }
    
    if(concat):
        resultPath = list()
        for i, o in enumerate(bestPathIteration["bestPaths"]):
            for y in range(len(o)-1):
                resultPath.append(o[y])
        resultPath.append(startPoint)
        
        return resultPath

    routes = {i+1:bestPathIteration["bestPaths"][i] for i in range(nbVehicules)}
    return routes, bestPathIteration["totLens"]