import pygame
from pygame.locals import *
import PySimpleGUI as sg

from mapa.grafo import *
from utils.params import *
from utils.interface import *

import json

# Carrega os dados do arquivo JSON
with open('./mapa/mapa.json') as json_file:
    data = json.load(json_file)


# Extrai as informações das cidades e das fronteiras
cities = data['cities']

# Função para obter o nome da cidade pelo ID
def get_city_name(city_id):
    for city in cities:
        if city['id'] == city_id:
            return city['name']
    return None

# Criação do Grafo
G, mapeamento, posicoes_cidade = gera_grafo('./mapa/mapa.json')

# Criação do dicionário para armazenar as posições dos nós
#posicoes_cidade = cidades_posicao(G)

# Inicialização do Pygame Mixer (áudio)
pygame.mixer.init()
pygame.mixer.music.load("./media/musica.mp3") # Carregamento da trilha sonora
pygame.mixer.music.set_volume(0.3) # Definição do volume da trilha sonora
pygame.mixer.music.play(-1) # Início da reprodução da trilha sonora em loop infinito

# Inicialização do Pygame
pygame.init()

# Criação da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WesterosNav")
sg.theme('DarkGrey') # Define um tema personalizado para a janela
font = ('Helvetica', 14) # Define a fonte e o tamanho do texto

# Carrega a imagem de fundo
background_image = pygame.image.load('./media/mapa-fundo.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


start_node, end_node, menor_caminho, distancia, caminho = -1, -1, [], 0, ""

def define_nodes():
    """
    Carrega a janela para receber os nós de origem e destino e calcula o caminho e distância mínimos usando Dijkstra
    """    
    
    global start_node, end_node, menor_caminho, distancia, caminho
    # Cria um layout customizado para a janela do PySimpleGUI
    layout = [[sg.Text('Cidade de origem:', font=font), sg.DropDown(opcoes_cidades(mapeamento), key='start_node', font=font)],
            [sg.Text('Cidade de destino:', font=font), sg.DropDown(opcoes_cidades(mapeamento), key='end_node', font=font)],
            [sg.Button('OK', font=font, button_color=('white', '#1E90FF'))]
            ]
    start_node, end_node = open_window(layout)

    menor_caminho, distancia = G.dijkstra(start_node, end_node)
    caminho = " -> ".join([mapeamento[id] for id in menor_caminho]) # Passa a lista de menor caminho para uma string com o nome das cidades


if __name__ == "__main__":


    # Chama a tela de definir os vértices a serem calculadas pela primeira vezs
    define_nodes()

    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique com o botão esquerdo do mouse
                    mouse_pos = pygame.mouse.get_pos()
                    if 10 <= mouse_pos[0] <= BUTTON_X + BUTTON_WIDTH and 10 <= mouse_pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                        define_nodes()

        # Limpa a tela
        screen.fill((0, 0, 0))

        # Desenha o fundo do mapa
        background_image = pygame.image.load('./media/mapa-fundo.jpg')
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background_image, (0, 0))

        # Desenha as arestas do grafo
        for u, v, _ in G.edges():
            draw_edge(screen, posicoes_cidade[u], posicoes_cidade[v])
            
            
        # Desenha os nós
        for node, pos in posicoes_cidade.items():
            if node == start_node:
                draw_node(screen, pos, END_COLOR)
            elif node == end_node:
                draw_node(screen, pos, START_COLOR)
            else:
                draw_node(screen, pos, (255, 255, 255))



        # Desenha os nós
        #for node, pos in posicoes_cidade.items():
        #    if node == start_node:
        #        draw_node(screen, pos, START_COLOR)
        #    elif node == end_node:
        #        draw_node(screen, pos, END_COLOR)
        #    else:
        #        draw_node(screen, pos, (255, 255, 255))

        # Desenha os textos na tela
        draw_text(screen, "WesterosNav", (10, 10), 200)
        draw_text(screen, "Cidade de Origem: {}".format(get_city_name(start_node)), (10, 40), 300)
        draw_text(screen, "Cidade de Destino: {}".format(get_city_name(end_node)), (10, 60), 300)
        draw_text(screen, "Caminho Mínimo: {}".format(caminho), (10, 90), 300)
        draw_text(screen, "Distância em Milhas: {}".format(str(distancia)), (10, 170), 200)

        # Desenha o botão
        draw_button(screen)

        # Desenha o caminho mínimo em azul
        for i in range(len(menor_caminho)-1):
            pygame.draw.line(screen, (0, 0, 255), posicoes_cidade[menor_caminho[i]], posicoes_cidade[menor_caminho[i+1]], 3)
            pygame.display.update()
            pygame.time.wait(500)

        # Atualiza a tela
        pygame.display.update()
