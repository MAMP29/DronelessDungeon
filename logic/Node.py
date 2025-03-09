
class Node:
    """ Representa un nodo del árbol """

    def __init__(self, estado, padre=None, operador=None, profundidad=0, costo=0):
        self.estado = estado
        self.padre = padre
        self.operador = operador
        self.profundidad = profundidad
        self.costo = costo