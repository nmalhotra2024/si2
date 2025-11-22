import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player vs Enemies")

clock = pygame.time.Clock()

# Load background image
# Make sure "background.png" exists in the same folder
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load sounds
# Ensure these files exist in your folder
pygame.mixer.music.load("background_music.mp3")   # background music
hit_sound = pygame.mixer.Sound("hit.wav")         # sound for collisions

# Start background music
pygame.mixer.music.play(-1)  # loop forever

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 50, 50)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Keep player on screen
        self.rect.clamp_ip(screen.get_rect())

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20))
        )
        # Random movement
        self.dx = random.choice([-3, -2, -1, 1, 2, 3])
        self.dy = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off edges
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

# Sprite groups
player = Player()
player_group = pygame.sprite.Group(player)

enemies = pygame.sprite.Group()
for _ in range(7):  # create 7 enemies
    enemies.add(Enemy())

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player + enemies
    player_group.update()
    enemies.update()

    # Check collisions
    collisions = pygame.sprite.spritecollide(player, enemies, False)
    if collisions:
        hit_sound.play()       # play hit sound
        score += 1
        print("Score:", score)

    # Draw background image
    screen.blit(background, (0, 0))

    # Draw player + enemies
    player_group.draw(screen)
    enemies.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
