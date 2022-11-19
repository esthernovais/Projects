import pygame
import time
from pygame import font
from random import randint, choice
from pygame import display
from pygame.transform import scale
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock

pygame.init()
fonte = font.SysFont('comicsans', 50)
disparo = 0
tamanho = 800, 600  # variável que absorve o tamanho do plano em X e Y
superficie = display.set_mode((tamanho))  # variável que absorve a contrução do plano.
display.set_caption('The Spider Man')  # funcão que escreve o nome da janela.

fundo = scale(load('Imagens/cidade.jpg'), tamanho)  # como a imagem é maior que o plano, usamos a função SCALE para transformar a imagem no tamanho do plano.

class HomemAranha(Sprite):  # criamos o primeiro sprint que irá compor o jogo, o objeto principal.
    def __init__(self, teia):
        super().__init__()  # defino essa função será usada em outras classes como herança.

        self.image = load('Imagens/homemaranha_small.png')  # carrego a imagem e em seguida tranfiro para uma variável.
        self.rect = self.image.get_rect()  # uso a função get_rect na imagem, onde irá me permitir o movimento no plano.
        self.velocidade = 2
        self.teia = teia

    def update(self):

        keys = pygame.key.get_pressed()  # recebe o movimento

        teias_fonte = fonte.render(
            f'Teias: {15 - len(self.teia)}',
            True,
            (255, 255, 255)
        )
        superficie.blit(teias_fonte, (20, 20))

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

    def soltarTeia(self):
        if len(self.teia) < 15:
            self.teia.add(
                Teia(*self.rect.center)
            )

class Teia(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self, x, y):
        super().__init__()

        self.image = load('Imagens/teia_small.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 1
        if self.rect.x > tamanho[0]:
            self.kill()

class Inimigo(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self):
        super().__init__()

        self.image = load('Imagens/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(800, randint(10, 500))  # retorna posição aleatoria.
        )

    def update(self):
        self.rect.x -= 0.1


class Inimigo(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    
    def __init__(self):
        super().__init__()

        self.image = load('Imagens/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(800, randint(10, 500))  # retorna posição aleatoria.
        )

    def update(self):
        
        self.rect.x -= 1

        if self.rect.x == 0:
            deu_ruim = fonte.render(
            'VOCÊ PERDEU !',
            True,
            (0, 0, 0)
        )
            superficie.blit(deu_ruim, (200, 200))
            display.update()
            
            time.sleep(3)
            exit()
            
        
class Chefao(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self):
        
        super().__init__()

        self.image = load('Imagens/inimigo_2.png')
        self.rect = self.image.get_rect(
            center=(800, 300)  # retorna posição aleatoria.
        )

    def update(self):
        self.rect.x -= 0.1

        if self.rect.x == 0:
            deu_ruim = fonte.render(
            'VOCÊ PERDEU !',
            True,
            (0, 0, 0)
        )
            superficie.blit(deu_ruim, (200, 200))
            display.update()
            
            time.sleep(3)
            exit()


# Espaço do display
grupo_inimigo = Group()
grupo_chefao = Group()
grupo_aranha = Group()
homem_aranha = HomemAranha(grupo_aranha)
grupo_geral = GroupSingle(homem_aranha)
grupo_inimigo.add(Inimigo())
grupo_chefao.add(Chefao())

round = 0
morte = 0
clock = Clock()

while True:

    clock.tick(120)
    if round % 120 == 0:
        grupo_inimigo.add(Inimigo())

    superficie.blit(fundo, (
        0, 0))  # Faço o Bit Blit na imagem no ponto 0,0 do plano definimo, com isso consigo inserir a imagem no jogo.
    grupo_geral.draw(superficie)  # Desenhar o objeto no plano

    if (morte < 15):
        grupo_inimigo.draw(superficie)
        grupo_inimigo.update()
        disparo = 0
    else:
        grupo_chefao.draw(superficie)
        grupo_chefao.update()

    grupo_aranha.draw(superficie)

    grupo_geral.update()
    grupo_aranha.update()

    for evento in event.get():  # Events
        if evento.type == QUIT:
            pygame.quit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                homem_aranha.soltarTeia()


    if groupcollide(grupo_aranha, grupo_inimigo, True, True):
        morte += 1

    if disparo == 10:
        
        deu_bom = fonte.render(
            'VOCÊ GANHOU !',
            True,
            (0, 0, 0)
        )
        superficie.blit(deu_bom, (200, 200))
        display.update()
        resposta = True
        time.sleep(3)
        exit()
    else:
        resposta = False

    if groupcollide(grupo_aranha, grupo_chefao, True, resposta):
        disparo += 1

    round += 1
    display.update()  # a função update atualiza os frames.