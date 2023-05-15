import PySimpleGUI as sg
import pygame
import random

from utils.params import *

def draw_node(screen, pos, color):
    """
    Desenha um nó no mapa do pygame
    """
    pygame.draw.circle(screen, color, pos, NODE_SIZE)
    # adiciona textura de folhas ao nó
    texture = pygame.image.load('./media/stark.jpg').convert_alpha()
    texture = pygame.transform.scale(texture, (NODE_SIZE*2, NODE_SIZE*2))
    screen.blit(texture, (pos[0]-NODE_SIZE, pos[1]-NODE_SIZE))

def draw_edge(screen, pos1, pos2):
    """
    Desenha uma aresta no mapa do pygame
    """
    pygame.draw.line(screen, EDGE_COLOR, pos1, pos2, 2)

def draw_text(screen, text, pos):
    """
    Desenha uma texto na tela do mapa do pygame
    """
    font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
    text_surface = font.render(text, True, (1, 13, 247))
    text_shadow = font.render(text, True, (200, 200, 200)) # adiciona sombra ao texto
    screen.blit(text_shadow, (pos[0]+2, pos[1]+2))
    screen.blit(text_surface, pos)

def cidades_posicao(grafo):
    """
    Determina a posição das cidades no mapa
    """
    node_positions = {}

    for i, node in enumerate(grafo.nodes()):
        x = random.randint(NODE_SIZE, WIDTH-NODE_SIZE)
        y = random.randint(NODE_SIZE, HEIGHT-NODE_SIZE)
        node_positions[node] = (x, y)

    return node_positions

def open_window(layout):
    """
    Cria a janela perguntando quais as cidades o usuário quer ver o caminho/distância
    """
    window = sg.Window('Selecione as cidades: ', layout)

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

    return start_node, end_node