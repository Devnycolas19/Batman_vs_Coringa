import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import texto_boas_vindas
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
mensagens = texto_boas_vindas(nome)

batmanParado = pygame.image.load("bases/batmanParado.png")
batmanPulando = pygame.image.load("bases/batmanPulando.png")
batmanAgachado = pygame.image.load("bases/batmanAgachado.png")
batmanParado = pygame.transform.scale(batmanParado, (110, 130))
batmanPulando = pygame.transform.scale(batmanPulando, (110, 130))
batmanAgachado = pygame.transform.scale(batmanAgachado, (120, 90))
carta = pygame.image.load("bases/carta1.png")
carta = pygame.transform.scale(carta, (40,60))
coringa = pygame.image.load("bases/coringa.png")
coringa = pygame.transform.scale(coringa, (160, 120))
morcegos = pygame.image.load("bases/morcegos.png")
morcegos = pygame.transform.scale(morcegos, (120, 70))

fonteMenu = pygame.font.SysFont("comicsans",18)
fonteTitulo = pygame.font.SysFont("comicsans", 46)
fonteBotao = pygame.font.SysFont("comicsans", 28)
fonteDicas = pygame.font.SysFont("comicsans", 24)

amareloBatman = (255, 220, 0)
cinzaEscuro = (25, 25, 25)
cinzaClaro = (70, 70, 70)

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
    posicaoXmorcegos = -150
    posicaoYmorcegos = 90
    velocidadeMorcegos = 2

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

            posicaoXmorcegos += velocidadeMorcegos
            if posicaoXmorcegos > 1050:
                posicaoXmorcegos = -150
                posicaoYmorcegos = random.choice([60, 90, 120, 150])

            if posicaoXCarta < -125:
                posicaoXCarta = 800
                pontos = pontos + 1
                velocidadeCarta = velocidadeCarta + 0.3
                posicaoYCarta = random.choice([470, 515])
        cartaGirando = pygame.transform.rotate(carta, giroCarta)                    
        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        
        imagemBatman = batmanParado
        if pulando:
            imagemBatman = batmanPulando
        elif agachado:
            imagemBatman = batmanAgachado
        tela.blit(morcegos, (posicaoXmorcegos, posicaoYmorcegos))
        tela.blit(imagemBatman, (posicaoXbatman,posicaoYbatman))
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
                dead(pontos)
                
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

def dead(pontos):
    while True:
        tela.blit(fundoDead, (0, 0))

        largura = tela.get_width()
        altura = tela.get_height()

        # Pontuação no canto superior esquerdo
        texto_pontos = fonteMenu.render(f"Pontuação: {pontos}", True, branco)
        tela.blit(texto_pontos, (30, 35))

        # Botão tentar novamente maior
        botaoTentar = pygame.Rect(300, 560, 400, 60)
        desenhar_botao("TENTAR NOVAMENTE", botaoTentar)

        # Aviso ESC
        aviso = fonteMenu.render("Aperte ESC para sair", True, branco)
        aviso_rect = aviso.get_rect(bottomright=(largura - 30, altura - 25))
        tela.blit(aviso, aviso_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoTentar.collidepoint(evento.pos):
                    jogar()

        pygame.display.update()
        relogio.tick(60)

def boas_vindas():
    while True:
        tela.blit(fundoStart, (0, 0))

        titulo = fonteMenu.render("Bem-vindo ao Batman vs Coringa", True, branco)
        tela.blit(titulo, (250, 80))

        y = 160
        for linha in mensagens:
            texto = fonteMenu.render(linha, True, branco)
            tela.blit(texto, (170, y))
            y += 40

        recorde = fonteMenu.render(
            f"Recorde: {nome_maior} - {maior_pontos} pontos - {dataJogada}",
            True,
            branco)
        tela.blit(recorde, (170, 430))

        botaoIniciar = pygame.Rect(390, 530, 220, 55)
        pygame.draw.rect(tela, branco, botaoIniciar)

        textoBotao = fonteMenu.render("INICIAR", True, preto)
        tela.blit(textoBotao, (455, 545))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoIniciar.collidepoint(evento.pos):
                    jogar()

        pygame.display.update()
        relogio.tick(60)


def desenhar_botao(texto, retangulo):
    mouse = pygame.mouse.get_pos()

    if retangulo.collidepoint(mouse):
        cor_botao = cinzaClaro
    else:
        cor_botao = cinzaEscuro

    pygame.draw.rect(tela, cor_botao, retangulo, border_radius=15)
    pygame.draw.rect(tela, amareloBatman, retangulo, 3, border_radius=15)

    texto_render = fonteBotao.render(texto, True, branco)
    texto_rect = texto_render.get_rect(center=retangulo.center)
    tela.blit(texto_render, texto_rect)


def tela_dicas():
    while True:
        tela.blit(fundoStart, (0, 0))

        largura = tela.get_width()
        altura = tela.get_height()

        # Painel central
        painel_x = 170
        painel_y = 70
        painel_largura = 660
        painel_altura = 520

        painel = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 190))
        tela.blit(painel, (painel_x, painel_y))

        pygame.draw.rect(
            tela,
            amareloBatman,
            (painel_x, painel_y, painel_largura, painel_altura),
            3,
            border_radius=15
        )

        # Título
        titulo = fonteTitulo.render("COMO JOGAR", True, amareloBatman)
        titulo_rect = titulo.get_rect(center=(largura // 2, 125))
        tela.blit(titulo, titulo_rect)

        # Regras
        linhas = [
            "W ou seta para cima: pular",
            "S ou seta para baixo: agachar",
            "SPACE: pausar o jogo",
            "ESC: voltar para o menu",
            "",
            "Carta baixa: pule para desviar",
            "Carta alta: agache para desviar",
            "",
            "Objetivo: desviar das cartas do Coringa",
            "e fazer a maior pontuação possível."
            "Para salvar Gotham."
        ]

        y = 190
        for linha in linhas:
            texto = fonteDicas.render(linha, True, branco)
            texto_rect = texto.get_rect(center=(largura // 2, y))
            tela.blit(texto, texto_rect)
            y += 34

        # Botão voltar
        botaoVoltar = pygame.Rect(390, 610, 220, 55)
        desenhar_botao("VOLTAR", botaoVoltar)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoVoltar.collidepoint(evento.pos):
                    return

        pygame.display.update()
        relogio.tick(60)


def start():
    while True:
        tela.blit(fundoStart, (0, 0))
        botaoIniciar = pygame.Rect(390, 520, 220, 55)
        botaoDicas = pygame.Rect(390, 590, 220, 55)
        desenhar_botao("INICIAR", botaoIniciar)
        desenhar_botao("DICAS", botaoDicas)
        largura = tela.get_width()
        altura = tela.get_height()
        recorde = fonteMenu.render(
            f"Recorde: {nome_maior} - {maior_pontos} pontos - {dataJogada}",
            True,
            branco
        )
        recorde_rect = recorde.get_rect(bottomleft=(30, altura - 25))
        tela.blit(recorde, recorde_rect)
        aviso = fonteMenu.render("ESC para sair", True, branco)
        aviso_rect = aviso.get_rect(bottomright=(largura - 30, altura - 25))
        tela.blit(aviso, aviso_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botaoIniciar.collidepoint(evento.pos):
                    jogar()

                elif botaoDicas.collidepoint(evento.pos):
                    tela_dicas()

        pygame.display.update()
        relogio.tick(60)
           
start()