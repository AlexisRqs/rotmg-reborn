import pygame
import sys
import math
import random

# game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
FONT_SIZE = 32
SCORE_POSITION = (10, 10)  # top left of the screen

# player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 100

# bullet settings
BULLET_SPEED = 10

# enemy settings
ENEMY_SPEED = 2
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1  # spawn an enemy every 1 second

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.health = PLAYER_HEALTH

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_s]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_a]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # boundary conditions
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT

    def shoot(self, bullets, mouse_pos):
        bullet = Bullet(self.rect.center, mouse_pos)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()

        dx, dy = target[0] - pos[0], target[1] - pos[1]
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize

        self.velocity = (dx * BULLET_SPEED, dy * BULLET_SPEED)

        self.rect.center = pos

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # remove if it leaves the visible screen
        if not (0 <= self.rect.x <= WINDOW_WIDTH and 0 <= self.rect.y <= WINDOW_HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(WINDOW_HEIGHT - self.rect.height)
        self.speed = ENEMY_SPEED

    def update(self):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > player.rect.y:
            self.rect.y -= self.speed

def main():
    pygame.init()
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Create a font object once and render() to create a Surface.
    font = pygame.font.Font(None, FONT_SIZE)  # Use the default font and a size of 32.

    global player
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    score = 0  # Start the score at 0.

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    player.shoot(bullets, event.pos)
                    all_sprites.add(bullets)
            if event.type == SPAWN_ENEMY_EVENT:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1  # Increase the score when an enemy is hit.

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            player.health -= 1
            if player.health <= 0:
                running = False

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        # Draw the health bar
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        BAR_COLOR = (255, 0, 0)  # Red
        BAR_BACKGROUND_COLOR = (50, 50, 50)  # Dark grey
        health_bar_position = (SCORE_POSITION[0], SCORE_POSITION[1])
        pygame.draw.rect(screen, BAR_BACKGROUND_COLOR, (*health_bar_position, BAR_WIDTH, BAR_HEIGHT))
        if player.health > 0:
            pygame.draw.rect(screen, BAR_COLOR, (*health_bar_position, player.health * 2, BAR_HEIGHT))

        score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
        score_position = (SCORE_POSITION[0], SCORE_POSITION[1] + BAR_HEIGHT + 10)  # Position the score below the health bar with extra space
        screen.blit(score_surface, score_position)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
