import pygame
from pygame.locals import *
from sys import exit
from random import randint
import tkinter as tk

global pause
pause = False
preto = (0,0,0)
vermelho = (200,0,0)
pygame.init()

# definindo sons;
clock = pygame.time.Clock()
musica_de_fundo = pygame.mixer.music.load('lofi.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
barulho_colisao = pygame.mixer.Sound('moeda.mp3')
pygame.mixer.Sound.set_volume(barulho_colisao,0.1)

# definindo velocidade, e tamanho da tela;
largura = 600
altura = 400

x_cobra = int(largura/1.5) 
y_cobra = int(altura/1.5)

velocidade = 8
x_controle = velocidade
y_controle = 0

x_maca = randint(40, 540)
y_maca = randint(50, 350)


# definindo fontes, comprimento da cobrinha;
pontos = 0
fonte = pygame.font.SysFont('arial', 40, bold=True, italic=True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')
relogio = pygame.time.Clock()
lista_cobra = []
comprimento_inicial = 5
morreu = False

 #####################################################
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
#####################################################


# Definindo alguns dos principais cases;
def quit_game():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, preto)
    return textSurface, textSurface.get_rect()

def unpause():
    pygame.mixer.music.unpause()
    global pause
    pause = False

def paused():
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms",100)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((largura/2),(altura/2))
    tela.blit(TextSurf, TextRect)

    while pause:
        
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if evento.type == KEYDOWN:
                if evento.key == K_p:
                    unpause()
                if evento.key == K_q:
                    pygame.quit()
                    exit()
                

        

        pygame.display.update()
        clock.tick(15)       

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x, y]
        #XeY[0] = x
        #XeY[1] = y

        pygame.draw.rect(tela, (0,255,0), (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura/2) 
    y_cobra = int(altura/2)
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 540)
    y_maca = randint(50, 350)
    morreu = False


# corpo principal do funcionamento do jogo;
while True:
    relogio.tick(30)
    tela.fill((200,255,255))
    
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, True, (0,0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT :
             pygame.quit()
             exit()
        
        if event.type == KEYDOWN:
            if event.key == K_p:
                pause = True
                paused()
                
            if event.key == K_q:
             pygame.quit()
             exit()
            if event.key == K_a or event.key == K_LEFT:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d or event.key == K_RIGHT:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w or event.key == K_UP:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_s or event.key == K_DOWN:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
        
    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra,y_cobra,20,20))
    maca = pygame.draw.rect(tela, vermelho, (x_maca,y_maca,20,20))
    
    if cobra.colliderect(maca):
        x_maca = randint(40, 540)
        y_maca = randint(50, 350)
        if pontos >= 10:
            pontos += 2
        else:
            pontos += 1
        barulho_colisao.play()
        comprimento_inicial = comprimento_inicial + 1

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Game over! Pressione a tecla R para jogar novamente'
        texto_formatado = fonte2.render(mensagem, True, (0,0,0))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((200,255,255))
            pygame.mixer.music.pause
            for event in pygame.event.get():
                if event.type == QUIT :
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_q :
                        pygame.quit()
                        exit()
                    if event.key == K_r:
                        reiniciar_jogo()

            ret_texto.center = (largura//2, altura//2) 
            tela.blit(texto_formatado, ret_texto)
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

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (380,40))
    
    pygame.display.update()