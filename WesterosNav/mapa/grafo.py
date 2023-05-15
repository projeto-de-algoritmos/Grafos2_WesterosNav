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
    
    def nodes(self):
        return list(self.adjacencia.keys())
    
    def vizinhos(self, vertice):
        if vertice in self.adjacencia:
            return [vizinho['vizinho'] for vizinho in self.adjacencia[vertice]]
        else:
            return []

    def edges(self):
        arestas = []
        for vertice, lista_adjacencia in self.adjacencia.items():
            for vizinho in lista_adjacencia:
                arestas.append((vertice, vizinho['vizinho'], vizinho['distancia']))
        return arestas

    def dijkstra(self, inicio, fim):
        dist = {vertice: float('inf') for vertice in self.nodes()}
        dist[inicio] = 0
        ant = {vertice: None for vertice in self.nodes()}

        nao_visit = set(self.nodes())

        while nao_visit:
            atual = min(nao_visit, key=lambda vertice: dist[vertice])
            nao_visit.remove(atual)

            if dist[atual] == float('inf'):
                break

            for vizinho in self.vizinhos(atual):
                for aresta in self.adjacencia[atual]:
                    if aresta['vizinho'] == vizinho:
                        alt = dist[atual] + aresta['distancia']
                        if alt < dist[vizinho]:
                            dist[vizinho] = alt
                            ant[vizinho] = atual

        caminho = []
        atual = fim
        while atual is not None:
            caminho.append(atual)
            atual = ant[atual]

        caminho.reverse()
        distancia = dist[fim]
        return caminho, distancia

def gera_grafo(path):
    # Cria o grafo e o dicionario de mapeamento
    grafo = Grafo()
    mapeamento = {}

    # Le o arquivo JSON
    with open(path, 'r') as f:
        data = json.load(f)

    # Adiciona as cidades como vertices e armazena o mapeamento
    for cidade in data['cities']:
        grafo.adiciona_vertice(cidade['id'])
        mapeamento[cidade['id']] = cidade['name']

    # Adiciona as fronteiras como arestas
    for fronteira in data['borders']:
        cidade1, cidade2 = fronteira['cidades']
        distancia = fronteira['distancia']
        grafo.adiciona_aresta(cidade1, cidade2, distancia)
    
    return grafo, mapeamento

def opcoes_cidades(mapeamento):
    return [(id, nome) for id, nome in mapeamento.items()]