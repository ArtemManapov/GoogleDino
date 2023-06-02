#-------------------- imports
import pygame
from random import randint
pygame.init()
#-------------------- imports


#-------------------- consts
DINO_IMG = 'dino.png'
DINO1_IMG = 'dino1.png'
DINO2_IMG = 'dino2.png'
GROUND_IMG = 'ground.png'
CACTUS_IMG = 'cactus.png'
BIRD_IMG = 'bird.png'
cadrs = 0
jump = False
score = 0
#-------------------- consts


#-------------------- classes
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width-10, height)
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(
        self, image, x, y, width, height, speed, ticks,
        k_up=pygame.K_UP
    ):
        super().__init__(image, x, y, width, height)
        self.ticks = ticks
        self.speed = speed
        self.k_up = k_up
        self.is_grounded = True
        self.jump_ticks = 0


    def update(self):
        if self.rect.y >= (640 - self.rect.height):
            self.is_grounded = True
            self.jump_ticks = 0
        else:
            self.is_grounded = False

        keys = pygame.key.get_pressed()
        if keys[self.k_up]:
            global jump
            jump = True
            if self.jump_ticks <= self.ticks:
                self.jump_ticks += 1
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
        else:
            if not self.is_grounded:
                self.rect.y += self.speed
            if self.is_grounded:
                jump = False
                
    def collide_rect(self, rect):
        return self.rect.colliderect(rect)
        
class Cactus(Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height)
        self.speed = speed

    def update(self):
        if self.rect.x > 0-self.rect.width:
            self.rect.x -= self.speed
        else:
            self.rect.x = 1280
            self.speed += 0.21

class Bird(Sprite):
    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height)
        self.speed = speed

    def update(self):
        if self.rect.x > 0-self.rect.width:
            self.rect.x -= self.speed
        else:
            self.place = randint(1, 3)
            self.rect.x = 1280
            if self.place == 1:
                self.rect.y = 588
            elif self.place == 2:
                self.rect.y = 560
            elif self.place == 3:
                self.rect.y = 490
            self.speed += 0.2
#-------------------- classes


#-------------------- window
window = pygame.display.set_mode((1280, 1024))
window.fill((255, 255, 255))
clock = pygame.time.Clock()
#-------------------- window


#-------------------- game
background = Sprite(GROUND_IMG, 0, 640, 3000, 10)
dino = Player(DINO_IMG, 200, 544, 80, 101, 3, 50)
cactus = Cactus(CACTUS_IMG, 1280, 575, 50, 70, 4)
bird = Bird(BIRD_IMG, 1280, 560, 55, 41, 4)
bird_sp = True

game_status = 'game'
while game_status != 'off':
    window.fill((255, 255, 255))
    cadrs += 1

    if game_status == 'game':
        score += 1
        my_font = pygame.font.SysFont('Arial', 30)
        score_txt = my_font.render(('score: ' + str(score)), True, (0, 0, 0))
        window.blit(score_txt, (50, 50))

        if jump == False:
            if cadrs%8 == 0:
                dino = Player(DINO1_IMG, 200, 544, 80, 101, dino.speed, dino.ticks)
            elif cadrs%10 == 0:
                dino = Player(DINO2_IMG, 200, 544, 80, 101, dino.speed, dino.ticks)
        elif jump == True:
            dino.image = pygame.transform.scale(pygame.image.load('dino.png'), (dino.rect.width, dino.rect.height))

        if cactus.rect.x < 640 and bird_sp == True:
            bird.reset()
            bird.rect.x = 1280
            cactus.speed -= 0.2
            bird_sp = False

        if bird_sp == False:
            bird.reset()

        if cactus.rect.x < 0-cactus.rect.width and dino.ticks > 30:
            dino.speed += 0.2
            dino.ticks -= 2
        elif cactus.rect.x < 0-cactus.rect.width and dino.ticks > 20:
            dino.speed += 0.2
            dino.ticks -= 1

        bird.update()
        background.reset()
        dino.update()
        dino.reset()
        cactus.update()
        cactus.reset()
        c1 = dino.collide_rect(cactus.rect)
        c2 = dino.collide_rect(bird.rect)
        if c1 or c2:
            game_status = 'result'
    elif game_status == 'result':
        window.fill((255, 255, 255))
        my_font = pygame.font.SysFont('Arial', 50)
        text = my_font.render('You Lose!', True, (255, 0, 0))
        score_txt = my_font.render(('Your score: ' + str(score)), True, (0, 0, 0))
        window.blit(text, ((1280//2)-100, 1024//2))
        window.blit(score_txt, ((1280//2)-95, 600))
        window.blit(pygame.image.load('dinoD.png'), (400, 1024//2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_status = 'off'

    clock.tick(60)
    pygame.display.update()
#-------------------- game
