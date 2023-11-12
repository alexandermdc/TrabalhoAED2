
import random
import pygame
import time
from config import *
from Sprites import *
from Solve import buscaInf

#Implementação principal para execução do jogo.
#Classe que encapsula a lógica do jogo.
class JogoPuzzle:
    #Configurações iniciais do jogo.
    def __init__(self):
        pygame.init()
        self.inicializa_tela()
        self.inicializa_temporizador()
        self.inicializa_variaveis_controle()
        self.inicializa_resolucao_automatica()

    def inicializa_tela(self):        
        self.screen = pygame.display.set_mode((largura_tela, altura_tela))
        pygame.display.set_caption(Titulo_tela)

    def inicializa_temporizador(self):
        # Inicializa temporização
        self.clock = pygame.time.Clock()

    def inicializa_variaveis_controle(self):
        self.tempo_aleatorio = 0
        self.cria_jogo_aleatorio = False
        self.inicia_jogo = False
        self.inicia_timer = 0
        self.tempo = 0
        self.ganhou = False
        self.sem_solucao = False

    def inicializa_resolucao_automatica(self):
        # Inicializa resolução automática
        self.resolve_aut = False
        self.numero_passos = False
        self.num_passos = None
        self.tempo_tela = None

    
    def cria_estado_final(self):
        #estado final desejado
        return [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def cria_lista_aleatoria_solucionavel(self):
        #solucionável para o puzzle
        puzzle = self.qd_lista.copy()
        random.shuffle(puzzle)

        if self.eh_solucionavel(puzzle):
            self.qd_lista = puzzle
        else:
            return self.cria_lista_aleatoria_solucionavel()

    def eh_solucionavel(self, puzzle):
        # Verifica se o é solucionável
        num_inversoes = 0

        for i in range(len(puzzle)):
            if puzzle[i] == 0:
                continue
            for j in range(i + 1, len(puzzle)):
                if puzzle[j] == 0:
                    continue
                if puzzle[i] > puzzle[j]:
                    num_inversoes += 1

        return num_inversoes % 2 == 0

    def desenha_quadrados(self):
        # Desenha os quadrados do jogo na tela
        self.quadrados = []
        for i in range(tamanho_jogo):
            self.quadrados.append([])
            for j in range(tamanho_jogo):
                indice = i * tamanho_jogo + j
                valor = str(self.qd_lista[indice]) if self.qd_lista[indice] != 0 else "vazio"
                self.quadrados[i].append(Area(self, j, i, valor))

    def inicia_novo_jogo(self):
        # Inicia um novo jogo
        self.sprites = pygame.sprite.Group()
        self.qd_lista = self.cria_estado_final()
        self.gabarito = self.cria_estado_final()
        self.tempo = 0
        self.inicia_jogo = False
        self.inicia_timer = False
        self.listaBotoes = [
            Botao(600, 120, 380, 55, "Novo Jogo", VERDE, PRETO),
            Botao(600, 200, 380, 55, "Começar", VERDE, PRETO),
            Botao(600, 280, 380, 55, "Solução Automática", VERDE, PRETO),
            Botao(600, 360, 380, 55, "Recomeçar", VERDE, PRETO)
        ]
        self.desenha_quadrados()

    def run(self):
        # Função principal que executa o loop do jogo
        self.jogando = True
        while self.jogando:
            self.clock.tick(FPS)
            self.eventos()
            self.update()
            self.draw()

    def update(self):
        # Atualiza os dados do jogo
        if self.inicia_jogo:
            if self.qd_lista == self.gabarito:
                self.inicia_jogo = False
                self.ganhou = True

            if self.inicia_timer:
                self.timer = time.time()
                self.inicia_timer = False

            self.tempo = time.time() - self.timer

        if self.cria_jogo_aleatorio:
            self.cria_lista_aleatoria_solucionavel()
            self.desenha_quadrados()
            self.tempo_aleatorio += 1

            if self.tempo_aleatorio > 50:
                self.cria_jogo_aleatorio = False

        if self.resolve_aut:
            if self.caminho != -1 and self.contador != len(self.caminho):
                self.qd_lista = self.caminho[self.contador]
                self.desenha_quadrados()
                self.contador += 1
                pygame.time.delay(700)
            elif self.caminho == -1 and self.passos == -1:
                self.resolve_aut = False
                self.sem_solucao = True
            else:
                self.resolve_aut = False
                self.numero_passos = True

        self.sprites.update()

    def draw(self):
        # Desenha os elementos na tela
        self.screen.fill(BRANCO)
        self.sprites.draw(self.screen)
        self.desenha_grade()

        for botao in self.listaBotoes:
            botao.draw(self.screen)

        ElemGraficos(780, 35, "%.2f" % self.tempo).draw(self.screen)

        if self.ganhou:
            if self.numero_passos:
                if self.tempo_tela is None:
                    self.tempo_tela = pygame.time.get_ticks()
                    self.num_passos = "Número de passos: " + str(self.passos)

                ElemGraficos(250, 580, self.num_passos).draw(self.screen)

                if pygame.time.get_ticks() - self.tempo_tela >= 7000:
                    self.ganhou = False
                    self.tempo_tela = None
                    self.numero_passos = False
            else:
                if self.tempo_tela is None:
                    self.tempo_tela = pygame.time.get_ticks()

                ElemGraficos(200, 580, "Você ganhou! Parabéns!!").draw(self.screen)

                if pygame.time.get_ticks() - self.tempo_tela >= 3000:
                    self.ganhou = False
                    self.tempo_tela = None

        if self.sem_solucao:
            if self.tempo_tela is None:
                self.tempo_tela = pygame.time.get_ticks()
            ElemGraficos(200, 580, "Sem solução :(").draw(self.screen)
            if pygame.time.get_ticks() - self.tempo_tela >= 3000:
                self.sem_solucao = False
                self.tempo_tela = None

        pygame.display.flip()

    def desenha_grade(self):       
        for i in range(-1, tamanho_jogo * tamanho_quadrado, tamanho_quadrado):
            pygame.draw.line(self.screen, CINZA_CLARO, (i, 0), (i, tamanho_jogo * tamanho_quadrado))

        for j in range(-1, tamanho_jogo * tamanho_quadrado, tamanho_quadrado):
            pygame.draw.line(self.screen, CINZA_CLARO, (0, j), (tamanho_jogo * tamanho_quadrado, j))

    def eventos(self):
        # Captura os eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.resolve_aut:
                mouseX, mouseY = pygame.mouse.get_pos()

                for i, quadrados in enumerate(self.quadrados):
                    for j, tile in enumerate(quadrados):
                        indice = i * tamanho_jogo + j
                        if tile.click(mouseX, mouseY):
                            self.mover_quadrado(indice, i, j)

                for botao in self.listaBotoes:
                    if botao.click(mouseX, mouseY):
                        self.processar_botao(botao)

    def mover_quadrado(self, indice, i, j):        
        if self.qd_lista[indice] != 0:
            if self.mover_direita(j, indice) or self.mover_esquerda(j, indice) or \
                    self.mover_cima(i, indice) or self.mover_baixo(i, indice):
                self.desenha_quadrados()

    def mover_direita(self, j, indice):        
        if j < tamanho_jogo - 1 and self.qd_lista[indice + 1] == 0:
            self.qd_lista[indice], self.qd_lista[indice + 1] = \
                self.qd_lista[indice + 1], self.qd_lista[indice]
            return True
        return False
    # Movevimenta os quadrado para os 4 lados
    def mover_esquerda(self, j, indice):        
        if j > 0 and self.qd_lista[indice - 1] == 0:
            self.qd_lista[indice], self.qd_lista[indice - 1] = \
                self.qd_lista[indice - 1], self.qd_lista[indice]
            return True
        return False

    def mover_cima(self, i, indice):        
        if i > 0 and self.qd_lista[indice - tamanho_jogo] == 0:
            self.qd_lista[indice], self.qd_lista[indice - tamanho_jogo] = \
                self.qd_lista[indice - tamanho_jogo], self.qd_lista[indice]
            return True
        return False

    def mover_baixo(self, i, indice):        
        if i < tamanho_jogo - 1 and self.qd_lista[indice + tamanho_jogo] == 0:
            self.qd_lista[indice], self.qd_lista[indice + tamanho_jogo] = \
                self.qd_lista[indice + tamanho_jogo], self.qd_lista[indice]
            return True
        return False
    
    #interação do usuário com os botões
    def processar_botao(self, botao):        
        if botao.texto == "Novo Jogo":
            self.inicia_novo_jogo()
            self.tempo_aleatorio = 0
            self.cria_jogo_aleatorio = True
        if botao.texto == "Recomeçar":
            self.inicia_novo_jogo()
        if botao.texto == "Começar" and self.qd_lista != self.gabarito:
            self.inicia_jogo = True
            self.inicia_timer = True
        if botao.texto == "Solução Automática" and self.qd_lista != self.gabarito:
            self.resolve_automaticamente()

    def resolve_automaticamente(self):        
        self.resolve_aut = True
        self.contador = 0
        self.caminho, self.passos = buscaInf(self.qd_lista)
        self.inicia_timer = True
        self.inicia_jogo = True


game = JogoPuzzle()
while True:
    game.inicia_novo_jogo()
    game.run()

