import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 800
FPS = 60
SHIP_SIZE = (60, 60)
ASTEROID_RADIUS = 20
POWERUP_SIZE = (40, 40)
SHIP_SPEED = 7
ASTEROID_SPEED = 5
POWERUP_SPEED = 4
SHIELD_DURATION = 5000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 30)

# Load ship images
ship_images = [pygame.transform.scale(pygame.image.load(f"sprites/ship/ship{i}.png"), SHIP_SIZE) for i in range(1, 5)]

# Game objects
class Asteroid:
    def __init__(self, x, y):
        self.radius = ASTEROID_RADIUS
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)

    def update(self, speed):
        self.y += speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        center = (self.x + self.radius, self.y + self.radius)
        pygame.draw.circle(surface, WHITE, center, self.radius)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, *POWERUP_SIZE)

    def update(self):
        self.y += POWERUP_SPEED
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)

# Game class
class Game:
    def __init__(self, death_count):
        self.ship_x = WIDTH // 2
        self.ship_y = HEIGHT - 100
        self.score = 0
        self.asteroids = []
        self.powerups = []
        self.shield_active = False
        self.shield_timer = 0
        self.death_count = death_count

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.ship_x > 0:
            self.ship_x -= SHIP_SPEED
        if keys[pygame.K_RIGHT] and self.ship_x < WIDTH - SHIP_SIZE[0]:
            self.ship_x += SHIP_SPEED

    def spawn_objects(self):
        if random.randint(1, 20) == 1:
            x = random.randint(0, WIDTH - ASTEROID_RADIUS * 2)
            self.asteroids.append(Asteroid(x, -ASTEROID_RADIUS * 2))
        if random.randint(1, 200) == 1:
            x = random.randint(0, WIDTH - POWERUP_SIZE[0])
            self.powerups.append(PowerUp(x, -POWERUP_SIZE[1]))

    def update_objects(self):
        ship_rect = pygame.Rect(self.ship_x, self.ship_y, *SHIP_SIZE)

        for asteroid in self.asteroids[:]:
            asteroid.update(ASTEROID_SPEED)
            if asteroid.y > HEIGHT:
                self.asteroids.remove(asteroid)
                self.score += 1
            elif asteroid.rect.colliderect(ship_rect):
                if not self.shield_active:
                    return False
                else:
                    self.asteroids.remove(asteroid)

        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(ship_rect):
                self.shield_active = True
                self.shield_timer = pygame.time.get_ticks()
                self.powerups.remove(powerup)
            elif powerup.y > HEIGHT:
                self.powerups.remove(powerup)

        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > SHIELD_DURATION:
            self.shield_active = False

        return True

    def draw(self):
        screen.fill(BLACK)

        # Draw ship image based on death count
        current_ship = ship_images[self.death_count % len(ship_images)]
        screen.blit(current_ship, (self.ship_x, self.ship_y))

        for asteroid in self.asteroids:
            asteroid.draw(screen)
        for powerup in self.powerups:
            powerup.draw(screen)

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.shield_active:
            shield_text = font.render("Shield ON", True, GREEN)
            screen.blit(shield_text, (WIDTH - 150, 10))

        pygame.display.flip()

# Game loop
def game_loop(death_count):
    game = Game(death_count)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.handle_input()
        game.spawn_objects()
        running = game.update_objects()
        game.draw()
        clock.tick(FPS)

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    final_score_text = font.render(f"Final Score: {game.score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)

    # Restart with next ship image
    game_loop(death_count + 1)

# Run
    game_loop(death_count)
    
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()