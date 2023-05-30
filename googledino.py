#-------------------- imports
import pygame
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
#-------------------- consts


#-------------------- classes
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(
        self, image, x=0, y=0, width=0, height=0,
        k_up=pygame.K_UP
    ):
        super().__init__(image, x, y, width, height)
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
            if self.jump_ticks <= 50:
                self.jump_ticks += 1
                self.rect.y -= 3
            else:
                self.rect.y += 3
        else:
            if not self.is_grounded:
                self.rect.y += 3
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
            self.speed += 0.2

#-------------------- classes


#-------------------- window
window = pygame.display.set_mode((1280, 1024))
window.fill((255, 255, 255))
clock = pygame.time.Clock()
#-------------------- window


#-------------------- game
background = Sprite(GROUND_IMG, 0, 640, 3000, 10)
dino = Player(DINO_IMG, 200, 544, 80, 101)
cactus = Cactus(CACTUS_IMG, 1280, 575, 50, 70, 4)


game_status = 'game'
while game_status != 'off':
    window.fill((255, 255, 255))
    cadrs += 1

    if game_status == 'game':
        if jump == False:
            if cadrs%8 == 0:
                dino = Player(DINO1_IMG, 200, 544, 80, 101)
            elif cadrs%10 == 0:
                dino = Player(DINO2_IMG, 200, 544, 80, 101)
        elif jump == True:
            dino.image = pygame.transform.scale(pygame.image.load('dino.png'), (dino.rect.width, dino.rect.height))


        background.reset()
        dino.update()
        dino.reset()
        cactus.update()
        cactus.reset()
        c1 = dino.collide_rect(cactus.rect)
        if c1:
            game_status = 'result'
    elif game_status == 'result':
        window.fill((255, 255, 255))
        my_font = pygame.font.Font(None, 50)
        text = my_font.render('You Lose!', True, (255, 0, 0))
        window.blit(text, ((1280//2)-100, 1024//2))
        window.blit(pygame.image.load('dinoD.png'), (400, 1024//2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_status = 'off'


    clock.tick(60)
    pygame.display.update()

#-------------------- game