import pygame
pygame.init()

screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Asteroid:
    def __init__(self, x, y):
        self.radius = 20
        self.x = x
        self.y = y

    def update(self):
        self.y += 5

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x + self.radius, self.y + self.radius), self.radius)

asteroids = [Asteroid(100, 0)]

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
