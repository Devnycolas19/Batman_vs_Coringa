import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Batman vs Coringa")
icone  = pygame.image.load("assets/logoBat.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("assets/beco.png")
fundoDead = pygame.image.load("assets/TelaDerrota.png")
fundoStart = pygame.image.load("assets/TelaInicio.png")

batman = pygame.image.load("assets/Batman.png")
batman = pygame.transform.scale(batman, (160,120))
carta = pygame.image.load("assets/carta1.png")
carta = pygame.transform.scale(carta, (40,60))
coringa = pygame.image.load("assets/coringa.png")
coringa = pygame.transform.scale(coringa, (160, 120))
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
pygame.mixer.music.load("assets/ironsound.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    tela.blit(fundo, (0, 0))
    posicaoXbatman = 130
    posicaoYbatman = 550
    posicaoXcoringa = 820
    posicaoYcoringa = 590
    posicaoXCarta = 780
    posicaoYCarta = 510
    velocidadeCarta = 2
    giroCarta = 0
    pontos = 0
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    chaoBatman = 520
    pulando = False
    noChao = True
    velocidadePulo = 0
    gravidade = 1
    abaixado = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                    if (evento.key == pygame.K_w or evento.key == pygame.K_UP) and noChao:
                        pulando = True
                        noChao = False
                        velocidadePulo = -18
                    elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                        abaixado = True
                    elif evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                            abaixado = False
                
        
        if pulando:
            posicaoYbatman += velocidadePulo
            velocidadePulo += gravidade
        if posicaoYbatman >= chaoBatman:
            posicaoYbatman = chaoBatman
            pulando = False
            noChao = True
            
            
        posicaoXCarta = posicaoXCarta - velocidadeCarta
        giroCarta += 5
        if posicaoXCarta < -125:
            posicaoXCarta = 800
            pontos = pontos + 1
            velocidadeCarta = velocidadeCarta + 1
            posicaoYCarta = random.choice([500, 580])
        cartaGirando = pygame.transform.rotate(carta, giroCarta)                    
        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        
        
        tela.blit(batman, (posicaoXbatman,posicaoYbatman))
        tela.blit(coringa, (posicaoXcoringa, posicaoYcoringa))
        tela.blit(cartaGirando, (posicaoXCarta, posicaoYCarta) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
            
        pixelsbatmanX = list(range(posicaoXbatman, posicaoXbatman+160))
        pixelsbatmanY = list(range(posicaoYbatman, posicaoYbatman+20))
        pixelsCartaX = list(range(posicaoXCarta, posicaoXCarta + 125))
        pixelsCartaY = list(range(posicaoYCarta, posicaoYCarta + 25))
        if  len( list( set(pixelsCartaY).intersection(set(pixelsbatmanY))) ) > dificuldade:
            if len( list( set(pixelsCartaX).intersection(set(pixelsbatmanX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
           
start()