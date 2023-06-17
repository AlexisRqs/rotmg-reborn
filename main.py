import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
PLAYER_SIZE = 50
PLAYER_SPEED = 1
PROJECTILE_SPEED = 1
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the player
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)

# Set up the projectiles
projectiles = []

# Start the game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mx, my = pygame.mouse.get_pos()
            # Calculate the direction vector from the player to the mouse
            dx, dy = mx - player.centerx, my - player.centery
            dist = math.hypot(dx, dy)
            dx, dy = dx / dist, dy / dist  # Normalize the direction vector
            # Create a new projectile and add it to the list
            projectiles.append((pygame.Rect(player.centerx, player.centery, 10, 10), dx, dy))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player.y += PLAYER_SPEED

    # Move the projectiles
    for proj, dx, dy in projectiles:
        proj.x += dx * PROJECTILE_SPEED
        proj.y += dy * PROJECTILE_SPEED

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player)
    for proj, _, _ in projectiles:
        pygame.draw.rect(screen, BLACK, proj)

    # Flip the display
    pygame.display.flip()
