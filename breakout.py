import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Define screen dimensions
WIDTH = 800
HEIGHT = 600
FPS = 60

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GOLD, [(10, 0), (15, 20), (0, 7), (20, 7), (5, 20)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = random.choice([-3, 3])
        self.speedy = -3

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speedx = -self.speedx
        if self.rect.top <= 0:
            self.speedy = -self.speedy
        if self.rect.bottom >= HEIGHT:
            return True
        return False

    def reset_ball(self):
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40
        self.speedx = random.choice([-3, 3])
        self.speedy = -3

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((90, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()
all_sprites.add(paddle, ball)

score = 0
font = pygame.font.Font(None, 36)

def show_message(message):
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before restarting the game

tries = 3

# Create bricks
for row in range(3):
    for column in range(8):
        brick = Brick(WHITE, column * 100, row * 30 + 80)
        all_sprites.add(brick)
        bricks.add(brick)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Check if the ball hits the paddle
    if pygame.sprite.collide_rect(ball, paddle):
        ball.speedy = -ball.speedy

    # Check if the ball hits the bottom
    if ball.update():
        tries -= 1
        ball.reset_ball()
        if tries == 0:
            show_message("You lost, you can play again")
            tries = 3
            # Reset bricks
            for brick in bricks:
                brick.kill()
                new_brick = Brick(WHITE, brick.rect.x, brick.rect.y)
                all_sprites.add(new_brick)
                bricks.add(new_brick)

    # Check if the ball hits a brick
    brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_collisions:
        score += len(brick_collisions)
        if len(bricks) == 0:
            show_message("Congratulations, You Won!")
            tries = 3
            # Reset bricks
            for row in range(3):
                for column in range(8):
                    brick = Brick(WHITE, column * 100, row * 30 + 80)
                    all_sprites.add(brick)
                    bricks.add(brick)

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw tries
    tries_text = font.render(f"Tries: {tries}", True, WHITE)
    screen.blit(tries_text, (10, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
