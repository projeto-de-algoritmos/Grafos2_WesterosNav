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

def draw_text(screen, text, pos, max_width):
    """
    Desenha uma texto na tela do mapa do pygame
    """
    font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
    words = text.split()  # Separa as palavras do texto
    lines = []
    current_line = ""
    
    for word in words:
        line_test = current_line + word + " "
        if font.size(line_test)[0] <= max_width:  # Verifica se a linha atual cabe na largura máxima
            current_line = line_test
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)
    
    # Desenha as linhas de texto na tela
    y = pos[1]
    for line in lines:
        text_surface = font.render(line, True, (1, 13, 247))
        text_shadow = font.render(line, True, (200, 200, 200)) # adiciona sombra ao texto
        screen.blit(text_shadow, (pos[0]+2, y+2))
        screen.blit(text_surface, (pos[0], y))
        y += font.get_height()


# Função para desenhar o botão com texto
def draw_button(screen):
    """
    Desenha um botão na tela do mapa do pygame
    """
    pygame.draw.rect(screen, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    font = pygame.font.Font(None, 24)
    text_surface = font.render("Outra Vez", True, WHITE)
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH/2, BUTTON_Y + BUTTON_HEIGHT/2))
    
    screen.blit(text_surface, text_rect)
    
    """
    def cidades_posicao(grafo):
        
       # Determina a posição das cidades no mapa
        
        node_positions = {}

        for i, node in enumerate(grafo.nodes()):
            x = random.randint(NODE_SIZE, WIDTH-NODE_SIZE)
            y = random.randint(NODE_SIZE, HEIGHT-NODE_SIZE)
            node_positions[node] = (x, y)

        return node_positions
    """

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
