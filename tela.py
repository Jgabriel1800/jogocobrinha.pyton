import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
pygame.mixer.music.set_volume(0.4)
musica_de_fundo = pygame.mixer.music.load('smw_castle_clear.wav')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('smw_1-up.wav')
barulho_colisao.set_volume(1.0)

largura = 640
altura = 480
x_cobra = largura / 2
y_cobra = altura / 2
velocidade = 5
x_controle = 20
y_controle = 0

x_maca = randint(40, 600)
y_maca = randint(50, 430)
pontos = 0
fonte = pygame.font.SysFont('arial', 40, True, True)  # texto na tela, em negrito e italico

cores_cobra = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255)]
indice_cor_atual = 0

def aumenta_cobra(lista_cobra, cor):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, cor, (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu, indice_cor_atual
    pontos = 0
    comprimento_inicial = 5
    x_cobra = largura / 2
    y_cobra = altura / 2
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False
    indice_cor_atual = 0

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Meu primeiro jogo')
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False

while True:
    relogio.tick(60)
    tela.fill((255, 255, 255))
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, False, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[K_a]:
        if x_controle == velocidade:
            pass
        else:
            x_controle = -velocidade
            y_controle = 0
    if keys[K_d]:
        if x_controle == -velocidade:
            pass
        else:
            x_controle = velocidade
            y_controle = 0
    if keys[K_w]:
        if y_controle == velocidade:
            pass
        else:
            y_controle = -velocidade
            x_controle = 0
    if keys[K_s]:
        if y_controle == -velocidade:
            pass
        else:
            y_controle = velocidade
            x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
    cobra = pygame.draw.rect(tela, cores_cobra[indice_cor_atual], (x_cobra, y_cobra, 20, 20))
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        barulho_colisao.play()
        comprimento_inicial += 1
        if pontos % 20 == 0:
            indice_cor_atual = (indice_cor_atual + 1) % len(cores_cobra)

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Game Over, pressione L para jogar novamente'
        texto_formatado = fonte2.render(mensagem, True, (0, 0, 0))
        ret_texto = texto_formatado.get_rect()
        morreu = True
        while morreu:
            tela.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_l:
                        reiniciar_jogo()
            ret_texto.center = (largura // 2, altura // 2)
            tela.blit(texto_formatado, (largura // 2, altura // 2))
            pygame.display.update()

    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura    
    if y_cobra > altura:
        y_cobra = 0

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra, cores_cobra[indice_cor_atual])

    tela.blit(texto_formatado, (450, 40))

    pygame.display.update()
