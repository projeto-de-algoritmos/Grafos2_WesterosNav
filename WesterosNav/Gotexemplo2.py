import networkx as nx
import random
import pygame
from pygame.locals import *
from math import sqrt
import json
import PySimpleGUI as sg

# Inicialização do Pygame Mixer
pygame.mixer.init()

# Carregamento da trilha sonora
pygame.mixer.music.load("musisca.mp3")

# Definição do volume da trilha sonora
pygame.mixer.music.set_volume(0.5)

# Início da reprodução da trilha sonora em loop infinito
pygame.mixer.music.play(-1)

def generate_graph(num_nodes, num_edges):
    G = nx.Graph()
    nodes = [i for i in range(num_nodes)]
    G.add_nodes_from(nodes)
    for _ in range(num_edges):
        u, v = random.sample(nodes, 2)
        G.add_edge(u, v)
    return G



# Parâmetros do jogo
WIDTH = 800
HEIGHT = 1000
NODE_SIZE = 15
START_COLOR = (255, 0, 0) # vermelho
END_COLOR = (84, 160, 86) # verde
EDGE_COLOR = (255, 255, 255)
FONT_SIZE = 35
FONT_STYLE = 'Ancient Medium.ttf' # fonte personalizada


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
G = generate_graph(23, 22)



# Define um tema personalizado para a janela
sg.theme('DarkGrey')

# Define a fonte e o tamanho do texto
font = ('Helvetica', 14)


# Cria uma lista com as opções de nó
node_options = [(str(node), node) for node in G.nodes()]

# Cria um layout customizado para a janela do PySimpleGUI
layout = [[sg.Text('(Cidade)Nó de origem:', font=font), sg.DropDown(node_options, key='start_node', font=font)],
          [sg.Text('(Cidade)Nó de destino:', font=font), sg.DropDown(node_options, key='end_node', font=font)],
          [sg.Button('OK', font=font, button_color=('white', '#1E90FF'))]]


# Cria a janela do PySimpleGUI
window = sg.Window('Selecione os nós', layout)

# Loop para ler os eventos da janela
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'OK':
        start_node = int(values['start_node'][0])
        end_node = int(values['end_node'][0])

        break

window.close()


# Criação do dicionário para armazenar as posições dos nós
node_positions = {}

for i, node in enumerate(G.nodes()):
    x = random.randint(NODE_SIZE, WIDTH-NODE_SIZE)
    y = random.randint(NODE_SIZE, HEIGHT-NODE_SIZE)
    node_positions[node] = (x, y)
    
# Atribuição de pesos aleatórios às arestas
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)


# Calcula o caminho mínimo usando o algoritmo de Dijkstra
shortest_path = dijkstra(G, start_node, end_node)

# Loop do jogo

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Limpa a tela
    screen.fill((0, 0, 0))

    # Desenha o fundo do mapa
    background_image = pygame.image.load('mapafundo.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))

    # Desenha os nós e as arestas do grafo
    for u, v in G.edges():
        pos1 = node_positions[u]
        pos2 = node_positions[v]
        draw_edge(screen, pos1, pos2)

    for node, pos in node_positions.items():
        if node == start_node:
            draw_node(screen, pos, START_COLOR)
        elif node == end_node:
            draw_node(screen, pos, END_COLOR)
        else:
            draw_node(screen, pos, (255, 255, 255))

    # Desenha o texto na tela
    draw_text(screen, "WesterosNav", (10, 10))
    draw_text(screen, "Starting city: {}".format(start_node), (10, 40))
    draw_text(screen, "Destination city: {}".format(end_node), (10, 70))
    draw_text(screen, 'Caminho mínimo:', (10, 110))

    # Desenha o caminho mínimo em azul
    for i in range(len(shortest_path)-1):
        pos1 = node_positions[shortest_path[i]]
        pos2 = node_positions[shortest_path[i+1]]
        pygame.draw.line(screen, (0, 0, 255), pos1, pos2, 3)
        pygame.display.update()
        pygame.time.wait(500)

    # Atualiza a tela
    pygame.display.update()

