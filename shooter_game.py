#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer 


class GameSprite (sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset (self):
        window.blit(self.image,(self.rect.x, self.rect.y)) 

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - 50:
            self.rect.x += self.speed
        '''if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < height - 50:
            self.rect.y += self.speed'''

    def fire (self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if  self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(50, width-50)
            lost = lost + 1

class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if  self.rect.y > height:
            self.kill()

#окно
width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
run = True
finish = False
rel_time = False
num_fire = 0
FPS = 60
count = 0
life = 3
font.init()
font1 = font.SysFont('Arial', 36)

win = font1.render('Ты выйграл!', True, (255, 255, 255))
lose = font1.render('Ты проиграл!', True, (255, 0, 0))

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
lost = 0
player = Player('rocket.png', width/2, height-80, 65, 65, 10)
bullets = sprite.Group()
fire_sound = mixer.Sound('fire.ogg')

asteroids = sprite.Group()
for i in range (1, 6):
    asteroid = Enemy('asteroid.png', randint(50, width-50), -40, 80, 50, randint (1,7))
    asteroids.add(asteroid)


monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy('ufo.png', randint(50, width-50), -40, 80, 50, randint (1,7))
    monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True 


    if finish != True: 
        window.blit(background, (0,0))

        text_win = font1.render('Счёт: ' + str(count), 1, (255, 255, 255))
        window.blit(text_win, (10, 20))

        text_lose  =  font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life  =  font1.render('Жизней: ' + str(life), 1, (255, 255, 255))
        window.blit(text_life, (10, 80))

        bullets.update()
        player.update()
        monsters.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                text_reload = font1.render('Идёт перезагрузка... ', 1, (255, 255, 255))
                window.blit(text_reload, (250, 350))
            else:
                num_fire = 0
                rel_time = False

        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            count = count + 1
            monster = Enemy('ufo.png', randint(50, width-50), -40, 80, 50, randint (1,7))
            monsters.add(monster)
        
        '''если коснулись'''
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1


        '''если проиграли'''
        if life == 0 or lost > 10:
            finish = True
            window.blit(lose, (200, 200))
        '''победа'''
        if count >= 10:
            finish = True
            window.blit(win, (200, 200))




    display.update()
    time.delay(50)