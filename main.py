import pygame
import random
import mysql.connector

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oscartime - Pygame Edition")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
game_over_font = pygame.font.SysFont("Arial", 64)

# Load images
player_img = pygame.image.load("./assets/player.png")
trash_img = pygame.image.load("./assets/trash.png")
virus_img = pygame.image.load("./assets/virus.png")  

# Resize images
player_img = pygame.transform.scale(player_img, (80, 80))
trash_img = pygame.transform.scale(trash_img, (40, 40))
virus_img = pygame.transform.scale(virus_img, (40, 40))



# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 8

trashes = []
viruses = []
score = 0
lives = 3

# Spawn event timers
SPAWN_TRASH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_TRASH, 1000)

SPAWN_VIRUS = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_VIRUS, 2000)

def draw_game_over():
    screen.fill((0, 0, 0))
    over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)

# Game loop
running = True
game_active = True

while running:
    if game_active:
        screen.fill((135, 206, 235))  # Sky blue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_TRASH:
                trashes.append([random.randint(0, WIDTH - 40), 0])
            elif event.type == SPAWN_VIRUS:
                viruses.append([random.randint(0, WIDTH - 40), 0])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 80:
            player_x += player_speed

        # Move trashes
        for trash in trashes[:]:
            trash[1] += 5
            if trash[1] > HEIGHT:
                trashes.remove(trash)
            elif abs(trash[0] - player_x) < 50 and abs(trash[1] - player_y) < 50:
                trashes.remove(trash)
                score += 1

        # Move viruses (obstacles)
        for virus in viruses[:]:
            virus[1] += 6
            if virus[1] > HEIGHT:
                viruses.remove(virus)
            elif abs(virus[0] - player_x) < 50 and abs(virus[1] - player_y) < 50:
                viruses.remove(virus)
                lives -= 1
                if lives <= 0:
                    game_active = False

        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Draw falling objects
        for trash in trashes:
            screen.blit(trash_img, trash)

        for virus in viruses:
            screen.blit(virus_img, virus)

        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

    else:
        draw_game_over()
        running = False


pygame.quit()
