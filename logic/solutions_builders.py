import itertools

"""
Esta clase proporciona funciones para reconstruir la solución obtenida por los algoritmos de búsqueda basándose en el conjunto de nodos visitados. 
Existen dos métodos principales para este propósito, dependiendo de la estructura utilizada para almacenar los nodos visitados:

1. Listas: Cuando el conjunto de visitados es una lista secuencial. Esto es útil para algoritmos como BFS y DFS (Depth-First Search), donde los nodos son explorados en un orden lineal. La reconstrucción de la solución se hace siguiendo la cadena de padres desde el nodo final hasta el nodo inicial.

2. Diccionarios: Cuando el conjunto de visitados es un diccionario, utilizado en algoritmos que priorizan nodos según su costo, UCS, Greedy Search y A*. En estos casos, se recomienda usar un diccionario para almacenar los nodos visitados junto con su costo y su nodo padre, permitiendo una reconstrucción eficiente del camino óptimo.
"""

def get_solution_from_list(rr, cc, visited, algo_type = 'bfs'):
    """
    Reconstruye la solución cuando el conjunto de nodos visitados es una lista.

    Parámetros:
    - rr, cc: Coordenadas del nodo objetivo al que se quiere llegar.
    - visited: Lista de nodos visitados en orden secuencial.
    - algo_type: Tipo de algoritmo utilizado ('bfs' o 'dfs'). (dfs no implementado aún)

    Retorna:
    - Una lista de coordenadas representando el camino desde el nodo inicial hasta el nodo final.
    """

    solution = []
    print(f"get_solucition: {len(visited)}")
    for nodo in visited:

        r, c, packages, cost, typemoven, parent = nodo

        print((r, c, packages, parent))
        # if r == rr and c == cc and lenpackage == len(packages):

        if r == rr and c == cc:

            solution.insert(0, [rr, cc])
            if parent is not None:
                rr = parent[0]
                cc = parent[1]
                # lenpackage -= 1
            else:
                print("Llegamos al nodo inicial")
                break

    return solution

def get_solution_from_dict(matriz, final_node, final_packages, visited):
    """
    Reconstruye la solución cuando el conjunto de nodos visitados está almacenado en un diccionario.

    Parámetros:
    - matriz: Matriz del entorno donde se ha realizado la búsqueda.
    - final_node: Nodo final desde donde se empieza la reconstrucción del camino.
    - final_packages: Conjunto de paquetes recogidos a lo largo del recorrido.
    - visited: Diccionario de nodos visitados donde cada clave es un estado y el valor es su nodo padre.

    Retorna:
    - Una lista de coordenadas representando el camino desde el nodo inicial hasta el nodo final.
    """
    solution = []

    # Empezamos desde el nodo final
    current_node = final_node
    current_packages = final_packages

    # Reconstruimos el camino hacia atrás
    while current_node is not None:
        solution.insert(0, [current_node[0], current_node[1]])

        # Verificamos si en este nodo recogimos un paquete
        if matriz[current_node[0], current_node[1]] == 4 and current_node in current_packages:
            # Quitamos este paquete para el siguiente paso de reconstrucción
            current_packages = frozenset([p for p in current_packages if p != current_node])

        # Buscamos el estado en el diccionario de visitados
        state = (current_node[0], current_node[1], current_packages)

        # Si no encontramos el estado exacto con estos paquetes, probamos con diferentes combinaciones
        if state not in visited:
            for p in range(len(final_packages) + 1):
                for pkg_combination in itertools.combinations(final_packages, p):
                    test_state = (current_node[0], current_node[1], frozenset(pkg_combination))
                    if test_state in visited:
                        state = test_state
                        current_packages = frozenset(pkg_combination)
                        break
                if state in visited:
                    break

        if state in visited:
            parent_info = visited[state]
            current_node = parent_info[0]  # El primer elemento es el parent
        else:
            print(f"Estado no encontrado en visitados: {state}")
            break

    print(f"Solución reconstruida con {len(solution)} pasos")
    return solution
