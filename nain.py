import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import os
import random

pygame.init()

largura_janela, altura_janela = 850, 800
chãox = 3
velcenario = 4
canoseparado = 150
canofrequencia = 1500
ultimocano = pygame.time.get_ticks() - canofrequencia
voar = True
gameover = False
pass_pipe = False
pontos = 0
dif,difi = 0,0
velo,veloci = 0,0
FPS = 60

colisão = pygame.mixer.Sound('flappy-bird-hit-sound-101soundboards.mp3')
fonte = pygame.font.SysFont('Arial', 30, True, True)
pygame.display.set_caption('Flappy Bird')
tela = pygame.display.set_mode((largura_janela, altura_janela))
clock = pygame.time.Clock()

pasta_principal = os.path.dirname(__file__)
pastasprites = os.path.join(pasta_principal,'sprites')

fundo = pygame.image.load('sprites/bg.png')
chão = pygame.image.load('sprites/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self,xbird,ybird):
        pygame.sprite.Sprite.__init__(self)
        self.imagensbird = []
        self.index = 0
        self.num1 = 0

        for i in range(1,4):
            img = pygame.image.load(f'sprites/bird{i}.png')
            self.imagensbird.append(img)
        self.image = self.imagensbird[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [xbird, ybird]
        self.vel = 0
        self.pulou = False
    def update(self):
        if voar == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.y < 630:
                self.rect.y += int(self.vel)
                
        if gameover == False:
            if self.vel < -5:
                self.pulou = True
            else:
                self.pulou = False

            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and self.pulou == False and self.rect.y > 80:
                self.pulou == True
                self.vel = -10

            self.num1 += 1
            cooldown = 5
            
            if self.num1 > cooldown:
                self.num1 = 0
                self.index += 1
                if self.index >= len(self.imagensbird):
                    self.index = 0  
            self.image = self.imagensbird[self.index]

            self.image = pygame.transform.rotate(self.imagensbird[self.index], self.vel * -4)
        else:
            self.image = pygame.transform.rotate(self.imagensbird[self.index], -90)

class Cano(pygame.sprite.Sprite):
    def __init__(self,x,y,posição):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/pipe.png')
        self.rect = self.image.get_rect()
        if posição == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(canoseparado / 2)]
        if posição == -1:
            self.rect.topleft = [x, y + int(canoseparado / 2)]
        
    def update(self):
        self.rect.x -= velcenario
        if self.rect.right < 0:
            self.kill()

birdgrupo = pygame.sprite.Group()
canogrupo = pygame.sprite.Group()

flappy = Bird(100,altura_janela//2)
birdgrupo.add(flappy)

def atualizar():
    global chãox,voar,gameover,ultimocano,pass_pipe,pontos,dif,difi,velo,veloci,canoseparado,velcenario
    if flappy.rect.y >= 630:
        gameover = True
        voar = False

    if pygame.sprite.groupcollide(birdgrupo, canogrupo, False, False):
        gameover = True

    if gameover == False and voar == True:
        tempo = pygame.time.get_ticks()
        if tempo - ultimocano > canofrequencia:
            canoaltura = random.randint(-100, 100)
            canofundo = Cano(largura_janela, int(altura_janela / 2) + canoaltura, -1)
            canotopo = Cano(largura_janela, int(altura_janela / 2) + canoaltura, 1)
            canogrupo.add(canofundo)
            canogrupo.add(canotopo)
            ultimocano = tempo

        chãox -= velcenario
        if abs(chãox) > 35:
            chãox = 0

        canogrupo.update()

        if len(canogrupo) > 0:
            if birdgrupo.sprites()[0].rect.left > canogrupo.sprites()[0].rect.left\
			and birdgrupo.sprites()[0].rect.right < canogrupo.sprites()[0].rect.right\
			and pass_pipe == False:
                pass_pipe = True
        if pass_pipe == True:
            if birdgrupo.sprites()[0].rect.left > canogrupo.sprites()[0].rect.right:
                pontos += 1
                pass_pipe = False
    if gameover == True:
        colisão.play()
        mensagem = 'Game over! pressione r para voltar a jogar'
        texto_formatado = fonte.render(mensagem, True, (0,0,0))
        ret_texto = texto_formatado.get_rect()
        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if gameover:
                            reiniciar()
            ret_texto.center = (largura_janela//2,altura_janela//2)
            tela.blit(texto_formatado, ret_texto)                
            pygame.display.update()
    keys = pygame.key.get_pressed()
    if keys[K_d]:
        dif = 1
    if keys[K_v]:
        velo = 1
    if difi:
        if canoseparado >= 150:
         canoseparado -= 0.05
        else:
            canoseparado -= 0.005
    if veloci:
        velcenario = 15
        canoseparado -= 0.025

def reiniciar():
    global pontos,ultimocano,gameover,voar,pass_pipe,canogrupo,difi,veloci,canoseparado
    ultimocano = pygame.time.get_ticks() - canofrequencia
    voar = True
    gameover = False
    pass_pipe = False
    pontos = 0
    flappy.rect.y = altura_janela//2
    canogrupo = pygame.sprite.Group()
    if dif:
        difi = 1
        canoseparado = 200
    if velo:
        veloci = 1

def desenhar(tela):
    print(canoseparado)
    tela.blit(fundo,(0,0))
    tela.blit(chão, (chãox, 668))
    birdgrupo.draw(tela)
    birdgrupo.update()
    canogrupo.draw(tela)
    mensagem = f'pontos:{pontos}'
    texto_formatado = fonte.render(mensagem, True, (0,0,0))
    tela.blit(texto_formatado, (largura_janela-200,10))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
    atualizar()
    desenhar(tela)
    clock.tick(FPS)
    pygame.display.flip()