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
icone  = pygame.image.load("bases/logoBat.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("bases/fundoFase.png")
fundoDead = pygame.image.load("bases/TelaDerrota.png")
fundoStart = pygame.image.load("bases/TelaInicio.png")

batman = pygame.image.load("bases/Batman.png")
batman = pygame.transform.scale(batman, (160,120))
carta = pygame.image.load("bases/carta1.png")
carta = pygame.transform.scale(carta, (40,60))
coringa = pygame.image.load("bases/coringa.png")
coringa = pygame.transform.scale(coringa, (160, 120))

fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    tela.blit(fundo, (0, 0))
    posicaoXbatman = 130
    posicaoYbatman = 450
    posicaoXcoringa = 820
    posicaoYcoringa = 450
    posicaoXCarta = 835
    posicaoYCarta = 470
    velocidadeCarta = 4
    giroCarta = 0
    pontos = 0

    dificuldade = 20
    chaoBatman = 450
    pulando = False
    agachado = False
    velocidadePulo = 0
    gravidade = 1
    abaixado = False
    pausado = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if (evento.key == pygame.K_w or evento.key == pygame.K_UP) and not pulando:
                    abaixado = False
                    pulando = True
                    agachado = False
                    velocidadePulo = -21
                elif evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                    abaixado = True
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_s or evento.key == pygame.K_DOWN:
                        abaixado = False
        if pulando:
            posicaoYbatman += velocidadePulo
            velocidadePulo += gravidade
        if posicaoYbatman >= chaoBatman:
            posicaoYbatman = chaoBatman
            pulando = False
            agachado = True
            
        if not pausado:
            posicaoXCarta = posicaoXCarta - velocidadeCarta
            giroCarta += 5
            if posicaoXCarta < -125:
                posicaoXCarta = 800
                pontos = pontos + 1
                velocidadeCarta = velocidadeCarta + 0.3
                posicaoYCarta = random.choice([470, 515])
        cartaGirando = pygame.transform.rotate(carta, giroCarta)                    
        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        
        
        tela.blit(batman, (posicaoXbatman,posicaoYbatman))
        tela.blit(coringa, (posicaoXcoringa, posicaoYcoringa))
        tela.blit(cartaGirando, (posicaoXCarta, posicaoYCarta) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
        textoPause = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(textoPause, (10, 15))    
        pixelsbatmanX = list(range(posicaoXbatman + 45, posicaoXbatman + 120))
        if abaixado and not pulando:
            pixelsbatmanY = list(range(posicaoYbatman + 80, posicaoYbatman + 145))
        else:
            pixelsbatmanY = list(range(posicaoYbatman + 35, posicaoYbatman + 145))
        pixelsCartaX = list(range(int(posicaoXCarta + 35), int(posicaoXCarta + 95)))
        pixelsCartaY = list(range(int(posicaoYCarta + 8),int( posicaoYCarta + 22)))
        if len(list(set(pixelsCartaY).intersection(set(pixelsbatmanY)))) > 5:
            if len(list(set(pixelsCartaX).intersection(set(pixelsbatmanX)))) > 5:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        if pausado:
            fontePause = pygame.font.SysFont(None, 80)
            textoPause = fontePause.render("PAUSE", True, (255, 255, 255))
            tela.blit(textoPause, (400, 300))
        
        pygame.display.update()
        relogio.tick(60)

def dead():

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