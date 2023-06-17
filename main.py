import pygame
import sys
import math
import random
from enum import Enum
import settings

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
FONT_SIZE = 32
SCORE_POSITION = (10, 10)  # top left of the screen

# Player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 100

# Bullet settings
BULLET_SPEED = 10

# Enemy settings
ENEMY_SPEED = 2
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1  # spawn an enemy every 1 second

# Game states
class GameState(Enum):
    START = 0
    PLAYING = 1
    GAME_OVER = 2


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
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # boundary conditions
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

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
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(WINDOW_HEIGHT - self.rect.height)
        self.speed = ENEMY_SPEED
        self.player = player  # Store the player instance

    def update(self):
        if self.rect.x < self.player.rect.x:
            self.rect.x += self.speed
        if self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < self.player.rect.y:
            self.rect.y += self.speed
        if self.rect.y > self.player.rect.y:
            self.rect.y -= self.speed


def show_start_menu(screen):
    font = pygame.font.Font(None, FONT_SIZE)
    title_surface = font.render("Shooting Game", True, (255, 255, 255))
    title_position = (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(title_surface, title_position)

    start_surface = font.render("Press Enter to Start", True, (255, 255, 255))
    start_position = (WINDOW_WIDTH // 2 - start_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(start_surface, start_position)

    settings_surface = font.render("Press S for Settings", True, (255, 255, 255))
    settings_position = (WINDOW_WIDTH // 2 - settings_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 100)
    screen.blit(settings_surface, settings_position)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    game_state = GameState.PLAYING
                    score = 0
                    return game_state, score
                elif event.key == pygame.K_s:
                    settings.show_settings_menu(screen)  # Call the settings menu from the settings module

    # Reset the game state and score
    game_state = GameState.START
    score = 0
    return game_state, score


def show_game_over_screen(screen, score):
    screen.fill((0, 0, 0))  # Clear the screen with black color

    font = pygame.font.Font(None, FONT_SIZE)
    game_over_surface = font.render("Game Over", True, (255, 255, 255))
    game_over_position = (WINDOW_WIDTH // 2 - game_over_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50)
    screen.blit(game_over_surface, game_over_position)

    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    score_position = (WINDOW_WIDTH // 2 - score_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 50)
    screen.blit(score_surface, score_position)

    restart_surface = font.render("Press R to Restart", True, (255, 255, 255))
    restart_position = (WINDOW_WIDTH // 2 - restart_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 100)
    screen.blit(restart_surface, restart_position)

    menu_surface = font.render("Press M for Menu", True, (255, 255, 255))
    menu_position = (WINDOW_WIDTH // 2 - menu_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 150)
    screen.blit(menu_surface, menu_position)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return "RESTART"
                elif event.key == pygame.K_m:
                    waiting = False
                    return "MENU"

    # Return the same state and score to continue the game
    return GameState.GAME_OVER, score, reset_game



def reset_game(player, all_sprites, bullets, enemies):
    player.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    player.health = PLAYER_HEALTH
    all_sprites.empty()
    all_sprites.add(player)  # Add player back to the sprite group
    bullets.empty()
    enemies.empty()
    return 0  # Return 0 as the updated score


def main():
    pygame.init()
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, FONT_SIZE)

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    game_state = GameState.START
    score = 0

    while True:
        if game_state == GameState.START:
            game_state, score = show_start_menu(screen)

        elif game_state == GameState.PLAYING:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        player.shoot(bullets, event.pos)
                        all_sprites.add(bullets)
                if event.type == SPAWN_ENEMY_EVENT:
                    enemy = Enemy(player)  # Pass player instance as parameter
                    enemies.add(enemy)
                    all_sprites.add(enemy)

            all_sprites.update()

            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 1

            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                player.health -= 1
                if player.health <= 0:
                    game_state = GameState.GAME_OVER

            screen.fill((0, 0, 0))
            all_sprites.draw(screen)

            BAR_WIDTH = 200
            BAR_HEIGHT = 20
            BAR_COLOR = (255, 0, 0)
            BAR_BACKGROUND_COLOR = (50, 50, 50)
            health_bar_position = (SCORE_POSITION[0], SCORE_POSITION[1])
            pygame.draw.rect(screen, BAR_BACKGROUND_COLOR,
                             (*health_bar_position, BAR_WIDTH, BAR_HEIGHT))
            if player.health > 0:
                pygame.draw.rect(screen, BAR_COLOR,
                                 (*health_bar_position, player.health * 2, BAR_HEIGHT))

            score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
            score_position = (SCORE_POSITION[0], SCORE_POSITION[1] + BAR_HEIGHT + 10)
            screen.blit(score_surface, score_position)

            pygame.display.flip()

        elif game_state == GameState.GAME_OVER:
            result = show_game_over_screen(screen, score)
            score = reset_game(player, all_sprites, bullets, enemies)
            if result == "MENU":
                game_state = GameState.START
                screen.fill((0, 0, 0))  # Clear the screen
            elif result == "RESTART":
                game_state = GameState.PLAYING
                


if __name__ == "__main__":
    main()
