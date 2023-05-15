import PySimpleGUI as sg
import pygame

from utils.params import *

def draw_node(screen, pos, color):
    pygame.draw.circle(screen, color, pos, NODE_SIZE)
    # adiciona textura de folhas ao nó
    texture = pygame.image.load('./media/stark.jpg').convert_alpha()
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

def open_window(layout):
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

    return start_node, end_node