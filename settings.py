import pygame
import sys
import json

# Settings file path
SETTINGS_FILE = "settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "volume": 0.5,
    "color": (255, 0, 0),
    "nickname": "Player"
}

# Load settings from file
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
    except FileNotFoundError:
        settings = DEFAULT_SETTINGS
    return settings

# Save settings to file
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def show_settings_menu(screen):
    font = pygame.font.Font(None, 32)

    settings = load_settings()
    selected_setting = "volume"  # Initialize the selected setting

    volume_text = font.render(f"Volume: {settings['volume']}", True, (255, 255, 255))
    volume_text_rect = volume_text.get_rect(center=(400, 200))

    color_text = font.render(f"Player Color: {settings['color']}", True, (255, 255, 255))
    color_text_rect = color_text.get_rect(center=(400, 250))

    nickname_text = font.render(f"Nickname: {settings['nickname']}", True, (255, 255, 255))
    nickname_text_rect = nickname_text.get_rect(center=(400, 300))

    save_text = font.render("Press Enter to Save", True, (255, 255, 255))
    save_text_rect = save_text.get_rect(center=(400, 400))

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Render the selected setting with a different color
        if selected_setting == "volume":
            volume_text = font.render(f"Volume: {settings['volume']}", True, (0, 255, 0))
        else:
            volume_text = font.render(f"Volume: {settings['volume']}", True, (255, 255, 255))
        screen.blit(volume_text, volume_text_rect)

        if selected_setting == "color":
            color_text = font.render(f"Player Color: {settings['color']}", True, (0, 255, 0))
        else:
            color_text = font.render(f"Player Color: {settings['color']}", True, (255, 255, 255))
        screen.blit(color_text, color_text_rect)

        if selected_setting == "nickname":
            nickname_text = font.render(f"Nickname: {settings['nickname']}", True, (0, 255, 0))
        else:
            nickname_text = font.render(f"Nickname: {settings['nickname']}", True, (255, 255, 255))
        screen.blit(nickname_text, nickname_text_rect)

        screen.blit(save_text, save_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    save_settings(settings)
                    running = False
                elif event.key == pygame.K_RIGHT:
                    if selected_setting == "volume":
                        settings['volume'] = min(settings['volume'] + 0.1, 1.0)
                    elif selected_setting == "color":
                        settings['color'] = (settings['color'][0] + 10, settings['color'][1], settings['color'][2])
                    elif selected_setting == "nickname":
                        pass  # Ignore the up arrow key for the nickname setting
                elif event.key == pygame.K_LEFT:
                    if selected_setting == "volume":
                        settings['volume'] = max(settings['volume'] - 0.1, 0.0)
                    elif selected_setting == "color":
                        settings['color'] = (settings['color'][0] - 10, settings['color'][1], settings['color'][2])
                    elif selected_setting == "nickname":
                        pass  # Ignore the down arrow key for the nickname setting
                elif event.key == pygame.K_UP:
                    if selected_setting == "volume":
                        selected_setting = "nickname"
                    elif selected_setting == "color":
                        selected_setting = "volume"
                    elif selected_setting == "nickname":
                        selected_setting = "color"
                elif event.key == pygame.K_DOWN:
                    if selected_setting == "volume":
                        selected_setting = "color"
                    elif selected_setting == "color":
                        selected_setting = "nickname"
                    elif selected_setting == "nickname":
                        selected_setting = "volume"
                elif event.key == pygame.K_BACKSPACE and selected_setting == "nickname":
                    settings['nickname'] = settings['nickname'][:-1]
                else:
                    if selected_setting == "nickname":
                        settings['nickname'] += event.unicode
