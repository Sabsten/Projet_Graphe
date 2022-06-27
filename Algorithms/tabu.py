def calcPathEfficiency(graph, paths, doPrint = True):
    nbVehicules = len(paths)
    size = len(graph)
    
    totLen = 0
    totLenVehicules = [0 for i in range(nbVehicules)]
    
    # Check data validity
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
    
    # Calculate path length
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

def tabu(graph, nbVehicules, nbIter):
    initGraph = graph
    startPoint = 0
    
    # Init tabou list (will store a path between 2 points)
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
            # print("-------")
            # print("0", len(visited))

            # Loop for every vehicule
            for v in range(nbVehicules):

                if(len(visited) >= len(graph)):
                    break

                # Worst case
                bestDistance = 99999999999
                bestNeighbour = startPoint

                # Search nearest neighbour
                for j in range(totPoints):
                    # Check if the path is not used (including other vehicules) + Check if path exists in tabu
                    if(currentElements[v] != j and j not in visited and (currentElements[v], j) not in tabuList[v]):
                        neighbour = graph[currentElements[v]][j]
                        if(neighbour <= bestDistance):
                            bestDistance = neighbour
                            bestNeighbour = j
                            tabuList[v].append((currentElements[v], j))
                            if(len(tabuList[v]) > maxTabuListSize):
                                tabuList[v].pop(0)

                # Could not find a solution => All combinaisons in tabou have been tried
                if(bestNeighbour == startPoint):
                    # print("NO SOLUTION", (currentElements[v], j, visited, tabuList))
                    # Search nearest neighbour
                    for j in range(totPoints):
                        # Check if the path is not used (including other vehicules) + Check if path exists in tabu
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
            # Return to start point
            bestPaths[v].append(startPoint)
            totLens[v] += graph[currentElements[v]][startPoint]
            bestDistances[v].append(graph[currentElements[v]][startPoint])
            
        worst, worstIndex, tot = calcPathEfficiency(initGraph, bestPaths, False)
        #print("ITER ", it, worst)
        if bestPathIteration.get("worst") is None or worst < bestPathIteration["worst"]:
            #print("New best for it", it, worst)
            bestPathIteration = {
                "bestPaths": bestPaths,
                "bestDistances": bestDistances,
                "totLens": totLens,
                "worst": worst
            }

    return (bestPathIteration["bestPaths"], bestPathIteration["bestDistances"], bestPathIteration["totLens"])