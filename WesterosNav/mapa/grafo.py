import json

class Grafo:
    """
    Classe que determina um grafo (lista de adjacência). Com os seguintes métodos:
    - Adiciona vértice
    - Adiciona aresta: vizinho e distância
    - Imprime o grafo
    - Nodes: retorna os nós
    - Edges: retorna as arestas
    - Vizinhos: pega os vizinhos de um vértice
    - Dijkstra: algoritmo para retornar menor caminho e a distância
    """
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

    def edges(self):
        arestas = []
        for vertice, lista_adjacencia in self.adjacencia.items():
            for vizinho in lista_adjacencia:
                arestas.append((vertice, vizinho['vizinho'], vizinho['distancia']))
        return arestas
    
    def vizinhos(self, vertice):
        if vertice in self.adjacencia:
            return [vizinho['vizinho'] for vizinho in self.adjacencia[vertice]]
        else:
            return []

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
    """
    A partir do arquivo json com o mapa, cria um grafo (cidades e fronteiras) e um mapeamento do id da cidade com seu nome
    """
    grafo = Grafo()
    mapeamento = {}
    posicoes = {}

    # Lê o arquivo JSON
    with open(path, 'r') as f:
        data = json.load(f)

    # Adiciona as cidades como vértices e armazena o mapeamento
    for cidade in data['cities']:
        cidade_id = cidade['id']
        grafo.adiciona_vertice(cidade_id)
        mapeamento[cidade_id] = cidade['name']

        # Verifica se a chave 'posicoes' existe no dicionário 'cidade'
        if 'posicoes' in cidade:
            cidade_posicao = cidade['posicoes']
        else:
            # Se a chave 'posicoes' não existir, emite um aviso e atribui uma posição padrão [0, 0]
            print(f"Aviso: A posição para a cidade ID {cidade_id} não foi encontrada.")
            cidade_posicao = [0, 0]

        posicoes[cidade_id] = cidade_posicao

    # Adiciona as fronteiras como arestas
    for fronteira in data['borders']:
        cidade1, cidade2 = fronteira['cidades']
        distancia = fronteira['distancia']
        grafo.adiciona_aresta(cidade1, cidade2, distancia)

    return grafo, mapeamento, posicoes

def opcoes_cidades(mapeamento):
    """
    Retorna a cidade com seu id
    """
    return [(id, nome) for id, nome in mapeamento.items()]
