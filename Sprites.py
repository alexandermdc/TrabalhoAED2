import pygame
from config import *

pygame.font.init()

#Área do jogo
class Area(pygame.sprite.Sprite):

    def __init__(self, game, x, y, texto):
        self.grupos = game.sprites
        pygame.sprite.Sprite.__init__(self, self.grupos)
        self.game = game
        self.image = pygame.Surface((tamanho_quadrado, tamanho_quadrado))
        self.x, self.y = x, y
        self.texto = texto
        self.rect = self.image.get_rect()
       
        if(self.texto != "vazio"):
            self.font = pygame.font.SysFont("Consolas",48) #fonte e tamanho
            font_surface = self.font.render(self.texto, True, PRETO)
            self.image.fill(VERDE)
            self.font_tam = self.font.size(self.texto)

            #Centralizar numeros no quadrado
            drawX = (tamanho_quadrado/2) - self.font_tam[0]/2
            drawY = (tamanho_quadrado/2) - self.font_tam[1]/2

            #quadradinhos dos números
            self.image.blit(font_surface,(drawX, drawY))
        else:
            #preenche o quadradinho com a cor do fundo quando estiver vazio
            self.image.fill(CINZA)

    #atualizando
    def update(self):
        self.rect.x = self.x *tamanho_quadrado
        self.rect.y = self.y *tamanho_quadrado

    
    def click(self, mouse_x, mouse_y):
        #posição do mouse
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    #verifica se a direita está vazi
    def checkDireita(self):
        return self.rect.x + tamanho_quadrado < tamanho_jogo * tamanho_quadrado

    #verifica se esquerda  está vazio
    def checkEsquerda(self):
        return self.rect.x - tamanho_quadrado >= 0

    #verifica se acima está vazio
    def checkCima(self):
        return self.rect.y - tamanho_quadrado >= 0

    #verifica se abaixo está vazio
    def checkBaixo(self):
        return self.rect.y + tamanho_quadrado < tamanho_jogo * tamanho_quadrado

#elementos gráficos
class ElemGraficos:
    def __init__(self, x, y, texto):
        self.x = x
        self.y = y
        self.texto = texto
    
    def draw(self,screen):
        font = pygame.font.SysFont("Consolas",48) #fonte
        texto = font.render(self.texto, True, VERDE)
        screen.blit(texto, (self.x,self.y))          


class Botao:
    def __init__(self, x, y, width, height, texto, cor, cor_texto):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto

    def draw(self, screen):       
        pygame.draw.rect(screen, self.cor, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 28) #escolhe a fonte
        texto = font.render(self.texto, True, self.cor_texto)
        self.font_tam = font.size(self.texto)
        
        drawX = self.x + (self.width/2) - self.font_tam[0]/2
        drawY = self.y + (self.height/2) - self.font_tam[1]/2        
        
        screen.blit(texto,(drawX, drawY))

    #checa se é "Clicavel"
    def click(self, mouse_x, mouse_y):
        #posição do mouse
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height