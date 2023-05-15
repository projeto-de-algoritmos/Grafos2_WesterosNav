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

# Le o arquivo JSON
with open('./mapa.json', 'r') as f:
    data = json.load(f)

# Cria o grafo e o dicionario de mapeamento
grafo = Grafo()
mapeamento = {}

# Adiciona as cidades como vertices e armazena o mapeamento
for cidade in data['cities']:
    grafo.adiciona_vertice(cidade['id'])
    mapeamento[cidade['id']] = cidade['name']

# Adiciona as fronteiras como arestas
for fronteira in data['borders']:
    cidade1, cidade2 = fronteira['cidades']
    distancia = fronteira['distancia']
    grafo.adiciona_aresta(cidade1, cidade2, distancia)

# Imprime o grafo e o mapeamento
grafo.imprime_grafo()
print(mapeamento)