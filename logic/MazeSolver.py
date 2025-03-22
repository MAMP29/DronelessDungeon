import heapq
from collections import deque
from typing import Deque

from logic.Node import Node
import numpy as np
import time
import pygame


class MazeSolver:
    """ Representa el laberinto original y lo resuelve con base a distintas funciones de búsqueda  """

    def __init__(self, maze_loader=None, maze_drawer=None):
        self.maze_drawer = maze_drawer
        if maze_loader:
            self.matriz = maze_loader.maze  # Matriz
            self.R, self.C = np.shape(self.matriz)  # Filas y Columnas
            self.sr, self.sc = map(int, np.where(self.matriz == 2))  # Lugar del buscador (dron)

            self.rowCowPaDeque = None  # Como algunas funciones no usan una cola directamente, inicializaremos este componente en el reset()

            # Variables para seguir el número de pasos tomados
            self.move_count = 0
            self.expanded_nodes = 0  # Contador de nodos expandidos
            self.nodes_left_in_layer = 1  # Considerando el nodo de inicio 2, son nodos pendientes en el nivel actual
            self.nodes_next_in_layer = 0  # Nodos que se visitarán en el siguiente nivel

            # Variable para seguir la meta
            self.number_of_objetives = np.count_nonzero(
                self.matriz == 4)  # Cuenta cuantos elementos son 4 en toda la matriz
            self.number_of_objetives_reached = 0
            self.reached_end = False

            # Matriz booleana para las posiciones, basada en la matriz original pero con puros ceros
            # self.visited = np.zeros_like(self.matriz, dtype=bool)        self.rowCowPaDeque: Deque[int] = deque()  # Especifica el tipo (int, str, etc.)

            # Movimiento, [0] arriba, [1] abajo, [2] derecha y [3] izquierda
            self.moves_row = np.array([-1, 1, 0, 0])
            self.moves_column = np.array([0, 0, 1, -1])
            self.type_moven = ["Arriba", "Abajo", "Derecha", "Izquierda"]
            self.type_box = ["Libre", "Obstáculo", "Inicio", "Campo electromagnético", "Paquete"]
            self.solution = []

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
        self.rowCowPaDeque.append((self.sr, self.sc, frozenset(), 0, -1, None))
        visited = [[self.sr, self.sc, frozenset(), 0, -1, None]]

        # visited[self.sr, self.sc] = True

        # print(f"Entrando a bfs {type(self.matriz)}")
        while len(self.rowCowPaDeque) > 0:  # Puede ser len(self.cq) > 0 pues se mueven igual
            # Extraemos las posiciones
            r, c, packages, cost, typemoven, parent = self.rowCowPaDeque.popleft()
            self.expanded_nodes += 1  # Se expandió un nodo

            #print("En ciclo" + type(self.matriz))

            if self.matriz[r, c] == 4 and (r, c) not in packages:
                # print(f"En paquete {type(self.matriz)}")

                # self.number_of_objetives_reached+=1

                new_packages = frozenset(list(packages) + [(r, c)])

                print(f"Número de objetivos alcanzados {len(packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                # self.matriz[r, c] = 0
                # print(self.matriz)
                # self.visited = TODO: HACER QUE LA POSICIÓN PASADA SEA UNA OPCIÓN PARA DEVOLVERSE
                new_state = (r,c, new_packages, cost, typemoven, parent)
                #if new_state not in visited:
                self.rowCowPaDeque.append(new_state)
                #visited.add(new_state)
                visited.insert(0,new_state)
                self.nodes_next_in_layer += 1

                #self.matriz[r, c] = 0
                #print(self.matriz)

                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    #print(f"S quedó en: ({r}, {c})")
                    print(f"SOLUCION: Nodo=({r},{c}) - paquetes={len(new_packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
                    self.get_solution(r, c, len(new_packages), visited)
                    break
                # print(f"En paquete 2 {type(self.matriz)}")

                # self.visited = TODO: HACER QUE LA POSICIÓN PASADA SEA UNA OPCIÓN PARA DEVOLVERSE
                new_state = (r, c, new_packages, cost, typemoven, parent)
                # if new_state not in visited:
                self.rowCowPaDeque.append(new_state)
                visited.insert(0, new_state)
                self.nodes_next_in_layer += 1

            #print(f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
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
            self.run_solution()
            return self.move_count

        print("No se encontró la solución")
        print(f"Movimientos {self.move_count}")
        return None

    def explore_neighbours(self, r, c, packages, cost, visited):
        # print(f"Explorando vecinos {type(self.matriz)}")

        for i in range(4):
            # Posición actual
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue

            new_state = (rr, cc, packages)

            # print(f"Ciclo explorando vecinos {type(self.matriz)}")
            # if new_state in visited: continue
            if any(nodo[:3] == new_state for nodo in visited): continue
            if self.matriz[rr, cc] == 1: continue

            if self.type_box[self.matriz[
                rr, cc]] == "Campo electromagnético": cost += 8  # Ahora tiene en cuenta el costo del campo electromagnético
            # print(f"MIRA MI CAMPO {self.type_box[self.matriz[rr, cc]] == "Campo electromagnético"}")

            #print(f"Vecino explorado: ({rr}, {cc}) ; Casilla: "+self.type_box[self.matriz[rr, cc]])
            new_state = new_state + (cost + 1, i, (int(r),int(c)))
            self.rowCowPaDeque.append(new_state)
            #visited.add(new_state)
            visited.insert(0,new_state)
            self.nodes_next_in_layer+=1

    def ucs(self):
        print("USANDO UCS")
        print(f"Numero de objetivos {self.number_of_objetives}")
        print(f"Número de objetivos alcanzados antes {self.number_of_objetives_reached}")
        print(f"columnas {self.C} y filas {self.R}")

        self.reset("ucs")

        visited = set()

        counter = 0

        # El costo va de primero como prioridad, luego le sigue un contador en caso de empate
        heapq.heappush(self.rowCowPaDeque, (0, counter, self.sr, self.sc, frozenset(), -1, None))
        visited.add((self.sr, self.sc, frozenset()))

        while len(self.rowCowPaDeque) > 0:

            cost, _, r, c, packages, typemoven, parent = heapq.heappop(self.rowCowPaDeque)
            self.expanded_nodes += 1  #

            # Verificar si este estado ya lo procesamos lo puse como control
            current_state = (r, c, packages)
            if current_state not in visited:
                continue  # Si ya lo visitamos, pasamos al siguiente

            if self.matriz[r, c] == 4 and (r, c) not in packages:
                # print(f"En paquete {type(self.matriz)}")

                # self.number_of_objetives_reached+=1

                new_packages = frozenset(list(packages) + [(r, c)])

                print(f"Número de objetivos alcanzados {len(packages)}")
                print(f"Paquete encontrado en: ({r}, {c})")

                # self.matriz[r, c] = 0
                # print(self.matriz)

                if len(new_packages) == self.number_of_objetives:
                    self.reached_end = True
                    # print(f"S quedó en: ({r}, {c})")
                    print(
                        f"SOLUCION: Nodo=({r},{c}) - paquetes={len(new_packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
                    break
                # print(f"En paquete 2 {type(self.matriz)}")

                counter += 1

                # self.visited = TODO: HACER QUE LA POSICIÓN PASADA SEA UNA OPCIÓN PARA DEVOLVERSE
                new_state = (r, c, new_packages)

                # if new_state not in visited: <- control
                counter += 1
                heapq.heappush(self.rowCowPaDeque, (cost, counter, r, c, new_packages, typemoven, parent))
                visited.add(new_state)

            print(
                f"Nodo=({r},{c}) - paquetes={len(packages)} - costo={cost} - movimiento={self.type_moven[typemoven]} - padre={parent}")
            self.explore_neighbours_usc(r, c, packages, cost, visited, counter)

        # print(f"Fuera de ciclo f{type(self.matriz)}")

        if self.reached_end:
            print(f"Terminado, profundidad: {self.move_count}")
            print(f"Nodos expandidos: {self.expanded_nodes}")
            return cost

        print("No se encontró la solución")
        print(f"Movimientos {self.move_count}")
        return None

    def explore_neighbours_usc(self, r, c, packages, cost, visited, counter):

        for i in range(4):
            # Posición actual
            rr = r + self.moves_row[i]
            cc = c + self.moves_column[i]

            if rr < 0 or cc < 0: continue
            if rr >= self.R or cc >= self.C: continue

            new_state = (rr, cc, packages)

            # print(f"Ciclo explorando vecinos {type(self.matriz)}")
            # if new_state in visited: continue
            if new_state in visited: continue
            if self.matriz[rr, cc] == 1: continue

            additional_cost = 1

            if self.type_box[self.matriz[
                rr, cc]] == "Campo electromagnético": additional_cost += 8  # Ahora tiene en cuenta el costo del campo electromagnético

            new_cost = additional_cost + cost
            counter += 1

            print(f"Vecino explorado: ({rr}, {cc}) ; Casilla: " + self.type_box[self.matriz[rr, cc]])

            heapq.heappush(self.rowCowPaDeque, (new_cost, counter, rr, cc, packages, i, (int(r), int(c))))

            visited.add(new_state)

    def get_solution(self, rr, cc, lenpackage, visited):
        print(f"get_solucition: {len(visited)}")
        for nodo in visited:
            r, c, packages, cost, typemoven, parent = nodo
            #if r == rr and c == cc and lenpackage == len(packages):
            if r == rr and c == cc:
                self.solution.insert(0, [rr, cc])
                if parent is not None:
                    rr = parent[0]
                    cc = parent[1]
                    #lenpackage -= 1
                else:
                    print("Llegamos al nodo inicial")
                    break



    def run_solution(self):
        print(f"run_solution: {len(self.solution)}")
        previous_r = 2
        previous_c = 1

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
