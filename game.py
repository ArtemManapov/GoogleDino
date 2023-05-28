import pygame
pygame.init()

# consts
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
ROCKET_IMG = 'rocket.png'
BALL_IMG = 'ball.png'
BG_COLOR = (64, 64, 64)
# consts

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=0, height=0):
        image = pygame.image.load(image)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(
        self, image, x=0, y=0, width=0, height=0, speed=5,
        k_up=pygame.K_UP, k_down=pygame.K_DOWN,
    ):
        super().__init__(image, x, y, width, height)
        self.speed = speed
        self.k_up = k_up
        self.k_down = k_down

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.k_up] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[self.k_down] and self.rect.y < (
            WINDOW_HEIGHT - self.rect.height
        ):
            self.rect.y += self.speed

class Ball(Sprite):
    dx = 5
    dy = 5

    def update(self, player_1, player_2):
        if self.rect.y <= 0:
            self.dy *= -1
        if self.rect.y >= (WINDOW_HEIGHT - self.rect.height):
            self.dy *= -1
        if self.rect.colliderect(player_1.rect):
            self.dx *= -1
        if self.rect.colliderect(player_2.rect):
            self.dx *= -1
        self.rect.x += self.dx
        self.rect.y += self.dy
        

    def is_outside(self):
        if self.rect.x < -self.rect.width:
            return 'left'
        elif self.rect.x > WINDOW_WIDTH:
            return 'right'
        else:
            return 'None'


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Пинг Понг')
window.fill(BG_COLOR)
clock = pygame.time.Clock()

player_left = Player(
    ROCKET_IMG, 5, 5, 30, 100, 5, pygame.K_w, pygame.K_s
)
player_right = Player(
    ROCKET_IMG, WINDOW_WIDTH - 35, WINDOW_HEIGHT - 105,
    30, 100, 5, pygame.K_UP, pygame.K_DOWN
)
ball = Ball(BALL_IMG, 40, 40, 32, 32)


game_status = 'game'
while game_status != 'off':
    window.fill(BG_COLOR)

    if game_status == 'game':
        ball_status = ball.is_outside()
        if ball_status == 'left':
            game_status = 'result'
            font = pygame.font.SysFont('Arial', 28)
            text = font.render('Победил 2 игрок!', True, (200, 200, 200))
        elif ball_status == 'right':
            game_status = 'result'
            font = pygame.font.SysFont('Arial', 28)
            text = font.render('Победил 1 игрок!', True, (200, 200, 200))
        
        ball.update(player_left, player_right)
        player_left.update()
        player_right.update()
        player_left.draw()
        player_right.draw()
        ball.draw()

    elif game_status == 'result':
        rect = text.get_rect()
        rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        window.blit(text, (rect.x, rect.y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_status = 'game'
            player_left = Player(
                ROCKET_IMG, 5, 5, 30, 100, 9, pygame.K_w, pygame.K_s
            )
            player_right = Player(
                                    ROCKET_IMG, WINDOW_WIDTH - 35, WINDOW_HEIGHT - 105,
                30, 100, 9, pygame.K_UP, pygame.K_DOWN
            )
            ball = Ball(BALL_IMG, 40, 40, 32, 32)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_status = 'off'

    clock.tick(60)
    pygame.display.update()

    


