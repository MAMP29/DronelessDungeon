import heapq
import time
from collections import deque
from time import sleep

import numpy as np
import pygame
from logic.solutions_builders import get_solution_from_list, get_solution_from_dict


class MazeSolver:
    """ Representa el laberinto original y lo resuelve con base a distintas funciones de búsqueda  """

    def __init__(self, maze_loader=None, maze_drawer=None):
        self.maze_drawer = maze_drawer
        if maze_loader:
            self.matriz = maze_loader.maze  # Matriz
            self.R, self.C = np.shape(self.matriz)  # Filas y Columnas
            self.sr, self.sc = map(int, np.where(self.matriz == 2))  # Lugar del buscador (dron)
            self.maze_packages = np.where(self.matriz == 4)
            self.maze_obstacles = np.where(self.matriz == 3)

            self.rowCowPaDeque = None  # Como algunas funciones no usan una cola directamente, inicializaremos este componente en el reset()

            # Variables para seguir el número de pasos tomados
            self.move_count = 0
            self.expanded_nodes = 0  # Contador de nodos expandidos
            self.nodes_left_in_layer = 1  # Considerando el nodo de inicio 2, son nodos pendientes en el nivel actual
            self.nodes_next_in_layer = 0  # Nodos que se visitarán en el siguiente nivel

            # Variable para seguir la meta
            self.number_of_objetives = np.count_nonzero(self.matriz == 4)  # Cuenta cuantos elementos son 4 en toda la matriz
            self.number_of_objetives_reached = 0
            self.reached_end = False


            # Movimiento, [0] arriba, [1] abajo, [2] derecha y [3] izquierda
            self.moves_row = np.array([-1, 1, 0, 0])
            self.moves_column = np.array([0, 0, 1, -1])
            self.type_moven = ["Arriba", "Abajo", "Derecha", "Izquierda"]
            self.type_box = ["Libre", "Obstáculo", "Inicio", "Campo electromagnético", "Paquete"]
            self.solution = []

    def execute_algorithm(self, algorithm_name):
        algorithms = {
            "BFS": self.bfs,
            "DFS": self.dfs,
            "UCS": self.ucs,
            "GBFS": self.gbfs,
            "A*": self.a_star,
        }

        if algorithm_name not in algorithms:
            return "Algoritmo no reconocido"

        print(f"Ejecutando {algorithm_name}...")
        report = algorithms[algorithm_name]()
        print("Construyendo reporte...")

        self.maze_drawer.reset_maze(self.sr, self.sc)

        if report:
            return (
                f"Ejecución por {algorithm_name} \n"
                f"Nodos expandidos: {report['nodos_expandidos']} \n "
                f"Profundidad: {report['profundidad']} \n "
                f"Tiempo: {report['tiempo']} \n "
                f"Coste: {report['costo'] if report['costo'] else 'No aplica'}"
            )
        else:
            return "No se encontró una solución"


    def reset(self, algorithm_type):
        """Resetea los valores para poder ejecutar el algoritmo nuevamente. Con base en la estructura de datos que se necesita para almacenar los nodos,
        reset la carga, por lo que es indispensable que esté en el inicio de la función"""
        if algorithm_type == "bst":
            self.rowCowPaDeque = deque()
        if algorithm_type == "ucs":
            self.rowCowPaDeque = []

        self.rowCowPaDeque.clear()
        self.move_count = 0
        self.expanded_nodes = 0
        self.nodes_left_in_layer = 1
        self.nodes_next_in_layer = 0
        self.number_of_objetives_reached = 0
        self.reached_end = False

    def bfs(self):
        print("USANDO BFS")
        print(f"Numero de objetivos {self.number_of_objetives}")
        print(f"Número de objetivos alcanzados antes {self.number_of_objetives_reached}")
        print(f"columnas {self.C} y filas {self.R}")

        self.reset("bst")

        # visited = set()
        # cada nodo tiene (row, column, packages, cost, type moven , parent)

        start_time = time.time()
        end_time = 0

        self.rowCowPaDeque.append((self.sr, self.sc, frozenset(), 0, -1, None))
        visited = [[self.sr, self.sc, frozenset(), 0, -1, None]]


        while len(self.rowCowPaDeque) > 0:  # Puede ser len(self.cq) > 0 pues se mueven igual
            # Extraemos las posiciones
            r, c, packages, cost, typemoven, parent = self.rowCowPaDeque.popleft()
            self.expanded_nodes += 1  # Se expandió un nodo


            if self.matriz[r, c] == 4 and (r, c) not in packages:

                new_packages = frozenset(list(packages) + [(r, c)])

                print(f"Número de objetivos alcanzados {len(packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                new_state = (r, c, new_packages, cost, typemoven, parent)
                self.rowCowPaDeque.append(new_state)
                visited.insert(0, new_state)
                self.nodes_next_in_layer += 1


                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    # print(f"S quedó en: ({r}, {c})")
                    print(f"SOLUCION: Nodo=({r},{c}) - paquetes={len(new_packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
                    end_time = time.time()
                    break
                # print(f"En paquete 2 {type(self.matriz)}")

            # print(f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
            self.explore_neighbours(r, c, packages, cost, visited)
            self.nodes_left_in_layer -= 1  # Quita un nodo restante
            print(f"nodos  {self.nodes_left_in_layer}")

            # Controla el avance al siguiente nivel, solo carga los que siguen al actual y suma profundidad
            if self.nodes_left_in_layer == 0:
                self.nodes_left_in_layer = self.nodes_next_in_layer
                self.nodes_next_in_layer = 0  # Reseteamos los nodos siguientes
                self.move_count += 1

        # print(f"Fuera de ciclo f{type(self.matriz)}")

        if self.reached_end:
            print(f"Terminado, profundidad: {self.move_count}")
            print(f"Nodos expandidos: {self.expanded_nodes}")
            self.solution = get_solution_from_list(r, c, visited, 'bfs')
            self.run_solution()
            return {
                "nodos_expandidos": self.expanded_nodes,
                "profundidad": self.move_count,
                "tiempo": end_time - start_time,
                "costo": None
            }

        print("No se encontró la solución")
        print(f"Movimientos {self.move_count}")
        return None

    def explore_neighbours(self, r, c, packages, cost, visited):
        for i in range(4):
            # Posición actual
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue

            new_state = (rr, cc, packages)

            if any(nodo[:3] == new_state for nodo in visited): continue
            if self.matriz[rr, cc] == 1: continue

            if self.type_box[self.matriz[rr, cc]] == "Campo electromagnético": cost += 8  # Tiene en cuenta el costo del campo electromagnético

            new_state = new_state + (cost + 1, i, (int(r), int(c)))
            self.rowCowPaDeque.append(new_state)
            visited.insert(0, new_state)
            self.nodes_next_in_layer += 1

    def dfs(self):
        print("USANDO DFS")
        print(f"Número de objetivos alcanzados antes {self.number_of_objetives_reached}")
        print(f"columnas {self.C} y filas {self.R}")
        package_coords = list(zip(map(int, self.maze_packages[0]), map(int, self.maze_packages[1])))
        print(f"COORDENADOS {package_coords}")

        self.reset('bst')  # Carga una deque

        start_time = time.time()
        end_time = 0

        # Estado inicial: (fila, columna, conjunto de paquetes recogidos, costo, tipo de movimiento, padre)
        self.rowCowPaDeque.append((self.sr, self.sc, frozenset(), 0, -1, None))

        # Diccionario de visitados: {(fila, columna, paquetes): (padre_coords, costo, tipo_movimiento)}
        visited = {(self.sr, self.sc, frozenset()): (None, 0, -1)}

        final_node = None
        final_packages = None

        while len(self.rowCowPaDeque) > 0:
            r, c, packages, cost, typemoven, parent = self.rowCowPaDeque.pop()  # Pop desde el final (correcto para DFS)
            self.expanded_nodes += 1

            print(f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven] if typemoven != -1 else 'Inicio'} - padre={parent}")

            # Verificamos si hemos alcanzado todos los objetivos
            if len(packages) == self.number_of_objetives:
                self.reached_end = True
                print(
                    f"SOLUCION: Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven] if typemoven != -1 else 'Inicio'} - padre={parent}")
                final_node = (r, c)
                final_packages = packages
                print("NODO FINAL", final_node)
                print("PAQUETES FINALES", final_packages)
                end_time = time.time()
                break

            # Si encontramos un paquete que no hemos recogido aún
            if self.matriz[r, c] == 4 and (r, c) not in packages:
                # Añadimos el paquete al conjunto
                new_packages = frozenset(list(packages) + [(r, c)])
                print(f"Número de objetivos alcanzados {len(new_packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                # Creamos el nuevo estado con los paquetes actualizados
                new_state = (r, c, new_packages)
                if new_state not in visited:
                    # Añadimos el nuevo estado a la pila
                    self.rowCowPaDeque.append((r, c, new_packages, cost, typemoven, parent))
                    # Actualizamos el diccionario de visitados
                    visited[new_state] = (parent, cost, typemoven)

                    # Continuamos al siguiente nodo del bucle para explorar desde el estado actualizado
                    continue

            # Exploramos los vecinos en el orden correcto (según los operadores definidos)
            self.explore_neighbours_dfs(r, c, packages, cost, visited)

        if self.reached_end:
            print(f"Nodos expandidos: {self.expanded_nodes}")
            self.solution = get_solution_from_dict(self.matriz, final_node, final_packages, visited)
            final_depth = len(self.solution) - 1  # La profundidad es el número de pasos (nodos - 1)
            self.run_solution()
            return {
                "nodos_expandidos": self.expanded_nodes,
                "profundidad": final_depth,
                "tiempo": end_time - start_time,
                "costo": None  # Añadimos el costo final a la respuesta
            }

        print("No se encontró la solución")
        print(f"Movimientos {self.move_count}")
        return None

    def explore_neighbours_dfs(self, r, c, packages, cost, visited):
        # Explorar vecinos en el orden definido por moves_row y moves_column
        # Esto garantiza que se respete el orden de los operadores
        for i in range(4):
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            # Verificaciones de límites y obstáculos
            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue
            if self.matriz[rr, cc] == 1: continue  # Evitamos obstáculos

            new_state = (rr, cc, packages)

            # Calculamos el costo adicional
            additional_cost = 1
            if self.matriz[rr, cc] == "Campo electromagnético": additional_cost += 8
            new_cost = cost + additional_cost

            # Si no hemos visitado este estado, lo añadimos a la pila
            if new_state not in visited:
                print(f"Vecino explorado: ({rr}, {cc}) ; Casilla: " + self.type_box[self.matriz[rr, cc]])
                # Añadir a la pila - para DFS agregamos al final para que sea el próximo en salir
                self.rowCowPaDeque.append((rr, cc, packages, new_cost, i, (int(r), int(c))))
                # Actualizamos visited con el formato correcto
                visited[new_state] = ((int(r), int(c)), new_cost, i)

    def ucs(self):
        print("USANDO UCS")
        print(f"Numero de objetivos {self.number_of_objetives}")
        print(f"Número de objetivos alcanzados antes {self.number_of_objetives_reached}")
        print(f"columnas {self.C} y filas {self.R}")
        self.reset("ucs")

        start_time = time.time()
        end_time = time.time()
        counter = 0
        # El costo va de primero como prioridad, luego le sigue un contador en caso de empate
        heapq.heappush(self.rowCowPaDeque, (0, counter, self.sr, self.sc, frozenset(), -1, None))

        # En lugar de usar una lista simple, usamos un diccionario para almacenar
        # los estados visitados con sus padres y otra información relevante
        visited = {(self.sr, self.sc, frozenset()): (None, 0, -1)}

        final_node = None
        final_cost = None
        final_packages = None

        while len(self.rowCowPaDeque) > 0:
            cost, _, r, c, packages, typemoven, parent = heapq.heappop(self.rowCowPaDeque)
            self.expanded_nodes += 1

            # Verificamos si ya encontramos una solución con menor costo
            current_state = (r, c, packages)

            if self.matriz[r, c] == 4 and (r, c) not in packages:
                new_packages = frozenset(list(packages) + [(r, c)])
                print(f"Número de objetivos alcanzados {len(packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    print(f"SOLUCION: Nodo=({r},{c}) - paquetes={len(new_packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
                    final_node = (r, c)
                    final_cost = cost
                    final_packages = new_packages
                    end_time = time.time()
                    break

                new_state = (r, c, new_packages)
                if new_state not in visited or cost < visited[new_state][1]:
                    counter += 1
                    heapq.heappush(self.rowCowPaDeque, (cost, counter, r, c, new_packages, typemoven, (int(r), int(c))))
                    visited[new_state] = ((int(r), int(c)), cost, typemoven)

            print(f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
            self.explore_neighbours_ucs(r, c, packages, cost, visited, counter)

        if self.reached_end:
            print(f"Terminado, costo: {final_cost}")
            print(f"Terminado, profundidad: {self.move_count}")
            print(f"Nodos expandidos: {self.expanded_nodes}")
            self.solution = get_solution_from_dict(self.matriz, final_node, final_packages, visited)
            print("NUEVA SOLUCION", self.solution)
            final_depth = len(self.solution) - 1  # La profundidad es el número de pasos (nodos - 1)
            self.run_solution()
            return {
                "nodos_expandidos": self.expanded_nodes,
                "profundidad": final_depth,
                "tiempo": end_time - start_time,
                "costo": final_cost
            }

        print("No se encontró la solución")
        return None

    def explore_neighbours_ucs(self, r, c, packages, cost, visited, counter):
        for i in range(4):
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue
            if self.matriz[rr, cc] == 1: continue

            new_state = (rr, cc, packages)

            additional_cost = 1
            if self.type_box[self.matriz[rr, cc]] == "Campo electromagnético": additional_cost += 8
            new_cost = additional_cost + cost

            if new_state not in visited or new_cost < visited[new_state][1]:
                counter += 1
                print(f"Vecino explorado: ({rr}, {cc}) ; Casilla: " + self.type_box[self.matriz[rr, cc]])
                heapq.heappush(self.rowCowPaDeque, (new_cost, counter, rr, cc, packages, i, (int(r), int(c))))
                visited[new_state] = ((int(r), int(c)), new_cost, i)


    def gbfs(self):
        print("USANDO GBFS")
        print(f"Numero de objetivos {self.number_of_objetives}")
        print(f"Número de objetivos alcanzados antes {self.number_of_objetives_reached}")
        print(f"columnas {self.C} y filas {self.R}")
        print(f"PAQUETES {self.maze_packages}")
        package_coords = list(zip(map(int, self.maze_packages[0]), map(int, self.maze_packages[1])))
        print(f"COORDENADOS {package_coords}")
        self.reset("ucs") # Sirve también

        start_time = time.time()
        end_time = 0
        counter = 0

        heapq.heappush(self.rowCowPaDeque, (0, counter, self.sr, self.sc, frozenset(), -1, None))

        visited = {(self.sr, self.sc, frozenset()): (None, 0, -1)}

        final_node = None
        final_heuristic_value = None
        final_packages = None

        while len(self.rowCowPaDeque) > 0:
            heuristic_value, _, r, c, packages, typemoven, parent = heapq.heappop(self.rowCowPaDeque)
            self.expanded_nodes += 1

            current_state = (r, c, packages)

            if self.matriz[r, c] == 4 and (r, c) not in packages:
                new_packages = frozenset(list(packages) + [(r, c)])
                print(f"Número de objetivos alcanzados {len(packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    print(f"SOLUCION: Nodo=({r},{c}) - paquetes={len(new_packages)} - valor heuristico={heuristic_value} - movimiento={self.type_moven[typemoven]} - padre={parent}")
                    final_node = (r, c)
                    final_heuristic_value = heuristic_value
                    final_packages = new_packages
                    end_time = time.time()
                    break

                new_state = (r, c, new_packages)
                if new_state not in visited or heuristic_value < visited[new_state][1]:
                    counter += 1
                    heapq.heappush(self.rowCowPaDeque, (heuristic_value, counter, r, c, new_packages, typemoven, (int(r), int(c))))
                    visited[new_state] = ((int(r), int(c)), heuristic_value, typemoven)

            print(f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={heuristic_value} - movimiento={self.type_moven[typemoven]} - padre={parent}")
            self.explore_neighbours_gbfs(r, c, packages, visited, counter, package_coords)

        if self.reached_end:
            print(f"Terminado, costo: {final_heuristic_value}")
            print(f"Nodos expandidos: {self.expanded_nodes}")
            self.solution = get_solution_from_dict(self.matriz, final_node, final_packages, visited)
            final_depth = len(self.solution) - 1
            self.run_solution()
            return {
                "nodos_expandidos": self.expanded_nodes,
                "profundidad": final_depth,
                "tiempo": end_time - start_time,
                "costo": final_depth
            }

        print("No se encontró la solución")
        return None


    def a_star(self):
        print("USANDO A*")
        print(f"Numero de objetivos {self.number_of_objetives}")
        package_coords = list(zip(map(int, self.maze_packages[0]), map(int, self.maze_packages[1])))
        self.reset("ucs")  # usa el mismo setup

        start_time = time.time()
        end_time = 0
        counter = 0
        start_state = (self.sr, self.sc, frozenset())
        h = self.manhattan_heuristic(self.sr, self.sc, package_coords)
        heapq.heappush(self.rowCowPaDeque, (h, 0, 0, self.sr, self.sc, frozenset(), -1, None))  # (f, g, h, r, c, paquetes, mov, padre)
        visited = {start_state: (None, 0, -1)}  # state: (parent, g, move_type)

        final_node = None
        final_cost = None
        final_packages = None

        while self.rowCowPaDeque:
            f, g, h_val, r, c, packages, typemoven, parent = heapq.heappop(self.rowCowPaDeque)
            self.expanded_nodes += 1
            current_state = (r, c, packages)

            if self.matriz[r, c] == 4 and (r, c) not in packages:
                new_packages = frozenset(list(packages) + [(r, c)])
                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    final_node = (r, c)
                    final_cost = g
                    final_packages = new_packages
                    end_time = time.time()
                    break
                packages = new_packages  # actualiza para seguir buscando más

            for i in range(4):
                rr = r + self.moves_row[i]
                cc = c + self.moves_column[i]
                if 0 <= rr < self.R and 0 <= cc < self.C and self.matriz[rr, cc] != 1:
                    new_state = (rr, cc, packages)
                    move_cost = 9 if self.matriz[rr, cc] == 3 else 1
                    new_g = g + move_cost
                    new_h = self.manhattan_heuristic(rr, cc, [p for p in package_coords if p not in packages])
                    new_f = new_g + new_h

                    if new_state not in visited or new_g < visited[new_state][1]:
                        counter += 1
                        heapq.heappush(self.rowCowPaDeque, (new_f, new_g, new_h, rr, cc, packages, i, (r, c)))
                        visited[new_state] = ((r, c), new_g, i)

        if self.reached_end:
            print(f"Terminado, costo total: {final_cost}")
            print(f"Nodos expandidos: {self.expanded_nodes}")
            self.solution = get_solution_from_dict(self.matriz, final_node, final_packages, visited)
            final_depth = len(self.solution) - 1
            self.run_solution()
            return {
                "nodos_expandidos": self.expanded_nodes,
                "profundidad": final_depth,
                "tiempo": end_time - start_time,
                "costo": final_cost
            }

        print("No se encontró la solución")
        return None


    def explore_neighbours_gbfs(self, r, c, packages, visited, counter, package_coords):
        for i in range(4):
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue
            if self.matriz[rr, cc] == 1: continue

            new_state = (rr, cc, packages)

            heuristic_value = self.manhattan_heuristic(rr, cc, package_coords)

            if new_state not in visited or heuristic_value < visited[new_state][1]:
                counter += 1
                print(f"Vecino explorado: ({rr}, {cc}) ; Casilla: " + self.type_box[self.matriz[rr, cc]])
                heapq.heappush(self.rowCowPaDeque, (heuristic_value, counter, rr, cc, packages, i, (int(r), int(c))))
                visited[new_state] = ((int(r), int(c)), heuristic_value, i)


    def manhattan_heuristic(self, r, c, package_coords):
        """
        Heuristica impusalda por la distancia de manhattan, del número de objetivos que hay, devuelve la menor, recibe
        las dos posiciones actuales
        """
        return min(abs(r - i[0]) + abs(c - i[1]) for i in package_coords)


    def run_solution(self):
        print(f"run_solution: {len(self.solution)}")
        previous_r = 2
        previous_c = 1

        packages_fixed = list(zip(map(int, self.maze_packages[0]), map(int, self.maze_packages[1])))
        obstacles_fixed = list(zip(map(int, self.maze_obstacles[0]), map(int, self.maze_obstacles[1])))

        self.maze_drawer.packages_fixed = packages_fixed
        self.maze_drawer.obstacles_fixed = obstacles_fixed

        screen = pygame.display.get_surface()  # Obtener la superficie de la pantalla

        for nodo in self.solution:
            r, c = nodo
            self.maze_drawer.move_charanter(previous_r, previous_c, r, c)
            previous_c = c
            previous_r = r

            # Redibujar todo el laberinto
            screen.fill((47, 40, 58))  # Color de fondo
            self.maze_drawer.draw_maze(screen)
            pygame.display.flip()
            pygame.time.wait(500)

            # Procesar eventos de pygame para evitar que la ventana se congele
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
