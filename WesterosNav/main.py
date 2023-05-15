import networkx as nx
import random
import pygame
from pygame.locals import *
from math import sqrt
import json
import PySimpleGUI as sg

from mapa.grafo import *
from utils.params import *
from utils.interface import *

# Criação do Grafo
G, mapeamento = gera_grafo('./mapa/mapa.json')

# Inicialização do Pygame Mixer
pygame.mixer.init()
pygame.mixer.music.load("./media/musica.mp3") # Carregamento da trilha sonora
pygame.mixer.music.set_volume(0.3) # Definição do volume da trilha sonora
pygame.mixer.music.play(-1) # Início da reprodução da trilha sonora em loop infinito

# Inicialização do Pygame
pygame.init()

# Criação da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
sg.theme('DarkGrey') # Define um tema personalizado para a janela
font = ('Helvetica', 14) # Define a fonte e o tamanho do texto

# Cria um layout customizado para a janela do PySimpleGUI
layout = [[sg.Text('(Cidade)Nó de origem:', font=font), sg.DropDown(opcoes_cidades(mapeamento), key='start_node', font=font)],
          [sg.Text('(Cidade)Nó de destino:', font=font), sg.DropDown(opcoes_cidades(mapeamento), key='end_node', font=font)],
          [sg.Button('OK', font=font, button_color=('white', '#1E90FF'))]
        ]

start_node, end_node = open_window(layout)

# Criação do dicionário para armazenar as posições dos nós
node_positions = {}

for i, node in enumerate(G.nodes()):
    x = random.randint(NODE_SIZE, WIDTH-NODE_SIZE)
    y = random.randint(NODE_SIZE, HEIGHT-NODE_SIZE)
    node_positions[node] = (x, y)

# Calcula o caminho mínimo usando o algoritmo de Dijkstra
shortest_path = G.dijkstra(start_node, end_node)

if __name__ == "__main__":
    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Limpa a tela
        screen.fill((0, 0, 0))

        # Desenha o fundo do mapa
        background_image = pygame.image.load('./media/mapa-fundo.jpg')
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background_image, (0, 0))

        # Desenha os nós e as arestas do grafo
        for u, v, _ in G.edges():
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