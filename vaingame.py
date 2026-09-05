import pygame
class Vaingame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # Clear the screen with black
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 frames per second
if __name__ == "__main__":
    game = Vaingame()
    game.run()
    pygame.quit()
