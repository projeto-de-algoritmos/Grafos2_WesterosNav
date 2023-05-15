import json

class Vertice:
    def __init__(self, id):
        self.id = id
        self.distancia = float('inf')
    
    def __repr__(self):
        return str(self.id)

class Grafo:
    def __init__(self):
        self.adjacencia = {}

    def adiciona_vertice(self, vertice):
        self.adjacencia[vertice] = []

    def adiciona_aresta(self, origem, destino, distancia):
        self.adjacencia[origem].append({'vizinho': destino, 'distancia': distancia})
        self.adjacencia[destino].append({'vizinho': origem, 'distancia': distancia})
    
    def imprime_grafo(self):
        for vertice, lista_adjacencia in self.adjacencia.items():
            print(f"Vertice {vertice}:")
            for vizinho in lista_adjacencia:
                print(f"\t Vizinho: {vizinho['vizinho']}, Distancia: {vizinho['distancia']}")