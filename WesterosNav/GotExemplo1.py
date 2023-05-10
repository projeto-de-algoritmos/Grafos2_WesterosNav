import networkx as nx
import random
import pygame
from pygame.locals import *
from math import sqrt

def generate_graph(num_nodes, num_edges):
    G = nx.Graph()
    nodes = [i for i in range(num_nodes)]
    G.add_nodes_from(nodes)
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)
    return G

#ou G = generate_graph(10, 15)

# Parâmetros do jogo
WIDTH = 800
HEIGHT = 600
NODE_SIZE = 20
START_COLOR = (244, 144, 138) # rosa
END_COLOR = (84, 160, 86) # verde
EDGE_COLOR = (255, 255, 255)
FONT_SIZE = 24
FONT_STYLE = 'freesansbold.ttf' # fonte personalizada


def draw_node(screen, pos, color):
    pygame.draw.circle(screen, color, pos, NODE_SIZE)
    # adiciona textura de folhas ao nó
    texture = pygame.image.load('stask.jpg').convert_alpha()
    texture = pygame.transform.scale(texture, (NODE_SIZE*2, NODE_SIZE*2))
    screen.blit(texture, (pos[0]-NODE_SIZE, pos[1]-NODE_SIZE))

# Função para desenhar uma aresta
def draw_edge(screen, pos1, pos2):
    pygame.draw.line(screen, EDGE_COLOR, pos1, pos2, 2)

# Função para calcular a distância entre dois pontos
def distance(pos1, pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

# Função para desenhar o texto na tela
def draw_text(screen, text, pos):
    font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
    text_surface = font.render(text, True, (1, 13, 247))
    text_shadow = font.render(text, True, (200, 200, 200)) # adiciona sombra ao texto
    screen.blit(text_shadow, (pos[0]+2, pos[1]+2))
    screen.blit(text_surface, pos)


# Função para calcular o caminho mínimo usando o algoritmo de Dijkstra
def dijkstra(graph, start, end):
    dist = {node: float('inf') for node in graph.nodes()}
    dist[start] = 0
    prev = {node: None for node in graph.nodes()}

    unvisited = set(graph.nodes())

    while unvisited:
        current = min(unvisited, key=lambda node: dist[node])
        unvisited.remove(current)

        if dist[current] == float('inf'):
            break

        for neighbor in graph.neighbors(current):
            alt = dist[current] + graph[current][neighbor]['weight']
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = current

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = prev[current]

    path.reverse()
    return path

# Inicialização do Pygame
pygame.init()

# Criação da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Geração do grafo
G = generate_graph(10, 15)

# Escolha aleatória do jogador e da cidade destino
start_node = random.choice(list(G.nodes()))
end_node = random.choice(list(G.nodes()))

# Criação do dicionário para armazenar as posições dos nós
node_positions = {}

for i, node in enumerate(G.nodes()):
    x = random.randint(NODE_SIZE, WIDTH-NODE_SIZE)
    y = random.randint(NODE_SIZE, HEIGHT-NODE_SIZE)
    node_positions[node] = (x, y)
    
# Atribuição de pesos aleatórios às arestas
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)


# Loop do jogo


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    background_image = pygame.image.load('fundo.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    # Desenha as arestas
    for u, v in G.edges():
        draw_edge(screen, node_positions[u], node_positions[v])

    # Desenha os nós
    for node, pos in node_positions.items():
        color = START_COLOR if node == start_node else END_COLOR if node == end_node else (255, 255, 255)
        draw_node(screen, pos, color)
        

    # Lê a entrada do usuário
    keys = pygame.key.get_pressed()
    if keys[K_a]:
        start_node = 'A'
    elif keys[K_b]:
        start_node = 'B'
    elif keys[K_c]:
        start_node = 'C'
    elif keys[K_d]:
        start_node = 'D'
    elif keys[K_e]:
        start_node = 'E'
    elif keys[K_f]:
        start_node = 'F'
    elif keys[K_g]:
        start_node = 'G'
    elif keys[K_h]:
        start_node = 'H'

    if keys[K_i]:
        end_node = 'I'
    elif keys[K_j]:
        end_node = 'J'
    elif keys[K_k]:
        end_node = 'K'
    elif keys[K_l]:
        end_node = 'L'
    elif keys[K_m]:
        end_node = 'M'
    elif keys[K_n]:
        end_node = 'N'
    elif keys[K_o]:
        end_node = 'O'
    elif keys[K_p]:
        end_node = 'P'



    # Calcula o caminho mínimo
    if start_node is not None and end_node is not None:
        path = dijkstra(G, start_node, end_node)
        


        # Desenha o caminho mínimo
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            draw_edge(screen, node_positions[path[i]], node_positions[path[i+1]])


        # Desenha o texto na tela
        draw_text(screen, "WESTEROS PATH SIM", (10, 10))
        draw_text(screen, "Starting city: {}".format(start_node), (10, 40))
        draw_text(screen, "Destination city: {}".format(end_node), (10, 70))
        draw_text(screen, "Distance: {}".format(nx.shortest_path_length(G, start_node, end_node)), (10, 100))

    else:
        # Desenha o texto na tela
        draw_text(screen, "WESTEROS PATH SIM", (10, 10))
        draw_text(screen, "Press 'A'-'H' to set starting city", (10, 40))
        draw_text(screen, "Press 'I'-'P' to set destination city", (10, 70))
        

    # Atualiza a tela
    pygame.display.update()

    # Atraso para limitar a taxa de atualização da tela
    pygame.time.delay(100)

