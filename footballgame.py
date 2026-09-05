import pygame
import sys
from pygame.math import Vector2

pygame.init()

# -----------------------------
# WINDOW SETTINGS
# -----------------------------
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Football League Supreme - OOP Edition")

CLOCK = pygame.time.Clock()
FPS = 60

# -----------------------------
# COLORS
# -----------------------------
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 255)
RED = (220, 50, 50)
YELLOW = (255, 215, 0)

# -----------------------------
# GAME STATES
# -----------------------------
STATE_MENU = "menu"
STATE_SETTINGS = "settings"
STATE_TEAM_NAMES = "team_names"
STATE_MODE_SELECT = "mode_select"
STATE_PLAYING = "playing"
STATE_GAMEOVER = "gameover"
STATE_TOURNAMENT_OVER = "tournament_over"

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
# ============================================================
# SECTION 2 — CORE CLASSES
# ============================================================

class Player:
    def __init__(self, x, y, color, is_cpu=False, role="striker", team="blue"):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.speed = 5
        self.stamina = 100
        self.max_stamina = 100
        self.is_cpu = is_cpu
        self.role = role
        self.team = team
        self.velocity = Vector2(0, 0)

    def move(self, direction):
        """Move the player based on a direction vector."""
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        # Keep inside field
        self.rect.x = clamp(self.rect.x, 0, WIDTH - self.rect.width)
        self.rect.y = clamp(self.rect.y, 0, HEIGHT - self.rect.height)

    def sprint(self, is_sprinting):
        """Adjust speed and stamina."""
        if is_sprinting and self.stamina > 0:
            self.speed = 8
            self.stamina = max(0, self.stamina - 0.5)
        else:
            self.speed = 5
            self.stamina = min(self.max_stamina, self.stamina + 0.2)

    def shoot(self, ball):
        """Kick the ball forward."""
        if self.rect.colliderect(ball.rect):
            ball.velocity = Vector2(12, 0)

    def pass_ball(self, ball, target_player):
        """Pass the ball toward a teammate."""
        if self.rect.colliderect(ball.rect):
            direction = Vector2(
                target_player.rect.centerx - self.rect.centerx,
                target_player.rect.centery - self.rect.centery
            ).normalize()
            ball.velocity = direction * 7

    def tackle(self, ball):
        """Knock the ball away if close."""
        if abs(self.rect.centerx - ball.rect.centerx) < 60 and \
           abs(self.rect.centery - ball.rect.centery) < 60:
            ball.velocity = Vector2(8, 0)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
        self.velocity = Vector2(0, 0)

    def update(self):
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        # Slow down gradually
        self.velocity *= 0.95

        # Bounce off walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity.y *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity.x *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = Vector2(0, 0)


class Goalkeeper:
    def __init__(self, x, y, team):
        self.rect = pygame.Rect(x, y, 40, 80)
        self.speed = 4
        self.team = team

    def update(self, ball):
        """Track the ball vertically only."""
        if ball.rect.centery > self.rect.centery:
            self.rect.y += self.speed
        elif ball.rect.centery < self.rect.centery:
            self.rect.y -= self.speed

        # Keep inside goal area
        self.rect.y = clamp(self.rect.y, 0, HEIGHT - self.rect.height)


class CPUController:
    """Balanced CPU behavior — not too strong, not too weak."""

    def update(self, player, ball, teammates, opponents):
        if player.role == "striker":
            self.update_striker(player, ball, opponents)
        else:
            self.update_defender(player, ball)

    def update_striker(self, player, ball, opponents):
        # Move toward ball
        direction = Vector2(
            ball.rect.centerx - player.rect.centerx,
            ball.rect.centery - player.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()

        player.move(direction)

        # Try to tackle
        player.tackle(ball)

        # Shoot if close to goal
        if player.team == "blue":
            if player.rect.centerx > WIDTH - 200:
                player.shoot(ball)
        else:
            if player.rect.centerx < 200:
                player.shoot(ball)

    def update_defender(self, player, ball):
        # Stay behind striker and track ball
        direction = Vector2(
            ball.rect.centerx - player.rect.centerx,
            ball.rect.centery - player.rect.centery
        )

        if direction.length() > 0:
            direction = direction.normalize()

        # Move slower than striker
        player.rect.x += direction.x * (player.speed - 1)
        player.rect.y += direction.y * (player.speed - 1)

        # Try to tackle
        player.tackle(ball)
        # ============================================================
# SECTION 3 — RENDERER CLASS
# ============================================================

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Arial", 60)
        self.font_medium = pygame.font.SysFont("Arial", 40)
        self.font_small = pygame.font.SysFont("Arial", 28)

    # --------------------------------------------------------
    # FIELD DRAWING
    # --------------------------------------------------------
    def draw_field(self):
        self.screen.fill(GREEN)

        # Center line
        pygame.draw.line(self.screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        # Center circle
        pygame.draw.circle(self.screen, WHITE, (WIDTH // 2, HEIGHT // 2), 100, 5)

        # Penalty boxes
        pygame.draw.rect(self.screen, WHITE, (0, HEIGHT // 2 - 150, 150, 300), 5)
        pygame.draw.rect(self.screen, WHITE, (WIDTH - 150, HEIGHT // 2 - 150, 150, 300), 5)

        # Goals
        pygame.draw.rect(self.screen, WHITE, (0, HEIGHT // 2 - 60, 20, 120))
        pygame.draw.rect(self.screen, WHITE, (WIDTH - 20, HEIGHT // 2 - 60, 20, 120))

    # --------------------------------------------------------
    # OBJECT DRAWING
    # --------------------------------------------------------
    def draw_player(self, player):
        pygame.draw.rect(self.screen, player.color, player.rect)

    def draw_ball(self, ball):
        pygame.draw.ellipse(self.screen, WHITE, ball.rect)

    def draw_goalkeeper(self, keeper):
        pygame.draw.rect(self.screen, YELLOW, keeper.rect)

    # --------------------------------------------------------
    # SCOREBOARD + STAMINA
    # --------------------------------------------------------
    def draw_scoreboard(self, score_left, score_right, time_left, team_left, team_right):
        score_text = self.font_large.render(f"{team_left} {score_left} - {score_right} {team_right}", True, WHITE)
        time_text = self.font_medium.render(f"Time: {int(time_left)}", True, WHITE)

        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        self.screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 90))

    def draw_stamina(self, players):
        y_offset = 10
        for p in players:
            bar_width = 100
            filled = int((p.stamina / p.max_stamina) * bar_width)
            pygame.draw.rect(self.screen, WHITE, (20, y_offset, bar_width, 10))
            pygame.draw.rect(self.screen, BLUE if p.team == "blue" else RED, (20, y_offset, filled, 10))
            y_offset += 20

    # --------------------------------------------------------
    # MENUS
    # --------------------------------------------------------
    def draw_menu(self):
        title = self.font_large.render("Football League Supreme", True, WHITE)
        play = self.font_medium.render("1. Play Match", True, WHITE)
        tournament = self.font_medium.render("2. Tournament", True, WHITE)
        settings = self.font_medium.render("3. Settings", True, WHITE)
        quit_game = self.font_medium.render("4. Quit", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        self.screen.blit(play, (WIDTH // 2 - play.get_width() // 2, 260))
        self.screen.blit(tournament, (WIDTH // 2 - tournament.get_width() // 2, 320))
        self.screen.blit(settings, (WIDTH // 2 - settings.get_width() // 2, 380))
        self.screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, 440))

    def draw_mode_select(self):
        title = self.font_large.render("Select Match Mode", True, WHITE)
        modes = [
            "1. 1v1 Human",
            "2. 1vCPU",
            "3. 2v2 Human",
            "4. 2vCPU",
            "5. Back"
        ]

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        y = 260
        for m in modes:
            text = self.font_medium.render(m, True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 60

    def draw_settings(self):
        title = self.font_large.render("Settings", True, WHITE)
        back = self.font_medium.render("Press B to go back", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(back, (WIDTH // 2 - back.get_width() // 2, 350))

    def draw_team_name_input(self, team_left, team_right):
        title = self.font_large.render("Enter Team Names", True, WHITE)
        left = self.font_medium.render(f"Left Team: {team_left}", True, WHITE)
        right = self.font_medium.render(f"Right Team: {team_right}", True, WHITE)
        info = self.font_small.render("Press ENTER to continue", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
        self.screen.blit(left, (WIDTH // 2 - left.get_width() // 2, 260))
        self.screen.blit(right, (WIDTH // 2 - right.get_width() // 2, 320))
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 400))

    # --------------------------------------------------------
    # GAME OVER + TOURNAMENT OVER
    # --------------------------------------------------------
    def draw_gameover(self, winner):
        title = self.font_large.render(f"{winner} Wins!", True, WHITE)
        info = self.font_medium.render("Press ENTER to return to menu", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 260))
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 340))

    def draw_tournament_over(self, winner):
        title = self.font_large.render(f"Tournament Champion: {winner}", True, WHITE)
        info = self.font_medium.render("Press ENTER to return to menu", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 260))
        self.screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 340))
        # ============================================================
# SECTION 4 — INPUT HANDLER CLASS
# ============================================================

class InputHandler:
    def __init__(self):
        self.typing_left = True  # Which team name is being typed

    # --------------------------------------------------------
    # PLAYER CONTROLS
    # --------------------------------------------------------
    def handle_player_input(self, player, keys):
        if player.is_cpu:
            return  # CPU players don't use keyboard

        direction = Vector2(0, 0)

        # Movement
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()

        # Sprint
        sprinting = keys[pygame.K_LSHIFT]
        player.sprint(sprinting)

        # Move
        player.move(direction)

    # --------------------------------------------------------
    # ACTIONS (SHOOT, PASS, TACKLE)
    # --------------------------------------------------------
    def handle_actions(self, player, ball, keys, teammates):
        if player.is_cpu:
            return

        # Shoot
        if keys[pygame.K_q]:
            player.shoot(ball)

        # Pass (to first teammate)
        if keys[pygame.K_e] and teammates:
            player.pass_ball(ball, teammates[0])

        # Tackle
        if keys[pygame.K_f]:
            player.tackle(ball)

    # --------------------------------------------------------
    # MENU NAVIGATION
    # --------------------------------------------------------
    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return "play"
            if event.key == pygame.K_2:
                return "tournament"
            if event.key == pygame.K_3:
                return "settings"
            if event.key == pygame.K_4:
                return "quit"
        return None

    # --------------------------------------------------------
    # MODE SELECT INPUT
    # --------------------------------------------------------
    def handle_mode_select(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return "1v1"
            if event.key == pygame.K_2:
                return "1vCPU"
            if event.key == pygame.K_3:
                return "2v2"
            if event.key == pygame.K_4:
                return "2vCPU"
            if event.key == pygame.K_5:
                return "back"
        return None

    # --------------------------------------------------------
    # SETTINGS INPUT
    # --------------------------------------------------------
    def handle_settings_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                return "back"
        return None

    # --------------------------------------------------------
    # TEAM NAME INPUT
    # --------------------------------------------------------
    def handle_team_name_input(self, event, team_left, team_right):
        if event.type == pygame.KEYDOWN:
            # Switch to next field
            if event.key == pygame.K_RETURN:
                if self.typing_left:
                    self.typing_left = False
                else:
                    return "done"

            # Backspace
            elif event.key == pygame.K_BACKSPACE:
                if self.typing_left:
                    team_left = team_left[:-1]
                else:
                    team_right = team_right[:-1]

            # Add characters
            else:
                char = event.unicode
                if char.isalnum() or char == " ":
                    if self.typing_left:
                        team_left += char
                    else:
                        team_right += char

        return team_left, team_right
        # ============================================================
# SECTION 5 — GAME CLASS (MAIN ENGINE)
# ============================================================

class Game:
    def __init__(self):
        self.renderer = Renderer(SCREEN)
        self.input_handler = InputHandler()
        self.cpu = CPUController()

        # Game state
        self.state = STATE_MENU

        # Team names
        self.team_left = "Blue"
        self.team_right = "Red"

        # Match data
        self.players = []
        self.goalkeepers = []
        self.ball = Ball()
        self.score_left = 0
        self.score_right = 0
        self.match_time = 90  # seconds

        # Tournament
        self.tournament_scores = {"left": 0, "right": 0}

        # Mode
        self.mode = None

    # --------------------------------------------------------
    # STATE MACHINE LOOP
    # --------------------------------------------------------
    def run(self):
        while True:
            if self.state == STATE_MENU:
                self.update_menu()
            elif self.state == STATE_MODE_SELECT:
                self.update_mode_select()
            elif self.state == STATE_SETTINGS:
                self.update_settings()
            elif self.state == STATE_TEAM_NAMES:
                self.update_team_names()
            elif self.state == STATE_PLAYING:
                self.update_playing()
            elif self.state == STATE_GAMEOVER:
                self.update_gameover()
            elif self.state == STATE_TOURNAMENT_OVER:
                self.update_tournament_over()

            pygame.display.flip()
            CLOCK.tick(FPS)

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------
    def update_menu(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            choice = self.input_handler.handle_menu_input(event)
            if choice == "play":
                self.state = STATE_MODE_SELECT
            elif choice == "tournament":
                self.state = STATE_TEAM_NAMES
            elif choice == "settings":
                self.state = STATE_SETTINGS
            elif choice == "quit":
                pygame.quit()
                sys.exit()

    # --------------------------------------------------------
    # MODE SELECT
    # --------------------------------------------------------
    def update_mode_select(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_mode_select()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            choice = self.input_handler.handle_mode_select(event)
            if choice == "1v1":
                self.mode = "1v1"
                self.start_match()
            elif choice == "1vCPU":
                self.mode = "1vCPU"
                self.start_match()
            elif choice == "2v2":
                self.mode = "2v2"
                self.start_match()
            elif choice == "2vCPU":
                self.mode = "2vCPU"
                self.start_match()
            elif choice == "back":
                self.state = STATE_MENU

    # --------------------------------------------------------
    # SETTINGS
    # --------------------------------------------------------
    def update_settings(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_settings()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            choice = self.input_handler.handle_settings_input(event)
            if choice == "back":
                self.state = STATE_MENU

    # --------------------------------------------------------
    # TEAM NAME INPUT
    # --------------------------------------------------------
    def update_team_names(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_team_name_input(self.team_left, self.team_right)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            result = self.input_handler.handle_team_name_input(
                event, self.team_left, self.team_right
            )

            if result == "done":
                self.state = STATE_MODE_SELECT
            else:
                self.team_left, self.team_right = result

    # --------------------------------------------------------
    # MATCH SETUP
    # --------------------------------------------------------
    def start_match(self):
        self.players = []
        self.goalkeepers = []
        self.ball.reset()
        self.score_left = 0
        self.score_right = 0
        self.match_time = 90

        # Goalkeepers
        self.goalkeepers.append(Goalkeeper(20, HEIGHT // 2 - 40, "left"))
        self.goalkeepers.append(Goalkeeper(WIDTH - 60, HEIGHT // 2 - 40, "right"))

        # Player spawning
        if self.mode == "1v1":
            self.players.append(Player(200, HEIGHT // 2, BLUE, is_cpu=False, team="blue"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2, RED, is_cpu=False, team="red"))

        elif self.mode == "1vCPU":
            self.players.append(Player(200, HEIGHT // 2, BLUE, is_cpu=False, team="blue"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2, RED, is_cpu=True, team="red"))

        elif self.mode == "2v2":
            self.players.append(Player(200, HEIGHT // 2 - 80, BLUE, is_cpu=False, role="striker"))
            self.players.append(Player(200, HEIGHT // 2 + 80, BLUE, is_cpu=False, role="defender"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2 - 80, RED, is_cpu=False, role="striker"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2 + 80, RED, is_cpu=False, role="defender"))

        elif self.mode == "2vCPU":
            self.players.append(Player(200, HEIGHT // 2 - 80, BLUE, is_cpu=False, role="striker"))
            self.players.append(Player(200, HEIGHT // 2 + 80, BLUE, is_cpu=False, role="defender"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2 - 80, RED, is_cpu=True, role="striker"))
            self.players.append(Player(WIDTH - 240, HEIGHT // 2 + 80, RED, is_cpu=True, role="defender"))

        self.state = STATE_PLAYING

    # --------------------------------------------------------
    # PLAYING STATE
    # --------------------------------------------------------
    def update_playing(self):
        keys = pygame.key.get_pressed()

        # Handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update players
        for p in self.players:
            if not p.is_cpu:
                self.input_handler.handle_player_input(p, keys)
                teammates = [t for t in self.players if t.team == p.team and t != p]
                self.input_handler.handle_actions(p, self.ball, keys, teammates)
            else:
                teammates = [t for t in self.players if t.team == p.team and t != p]
                opponents = [t for t in self.players if t.team != p.team]
                self.cpu.update(p, self.ball, teammates, opponents)

        # Update goalkeepers
        for g in self.goalkeepers:
            g.update(self.ball)

        # Update ball
        self.ball.update()

        # Check goals
        if self.ball.rect.left <= 0:
            self.score_right += 1
            self.ball.reset()

        if self.ball.rect.right >= WIDTH:
            self.score_left += 1
            self.ball.reset()

        # Timer
        self.match_time -= 1 / FPS
        if self.match_time <= 0:
            winner = self.team_left if self.score_left > self.score_right else self.team_right
            self.state = STATE_GAMEOVER
            self.winner = winner

        # DRAW EVERYTHING
        self.renderer.draw_field()

        for g in self.goalkeepers:
            self.renderer.draw_goalkeeper(g)

        for p in self.players:
            self.renderer.draw_player(p)

        self.renderer.draw_ball(self.ball)
        self.renderer.draw_scoreboard(self.score_left, self.score_right, self.match_time, self.team_left, self.team_right)
        self.renderer.draw_stamina(self.players)

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------
    def update_gameover(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_gameover(self.winner)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_MENU

    # --------------------------------------------------------
    # TOURNAMENT OVER
    # --------------------------------------------------------
    def update_tournament_over(self):
        SCREEN.fill(BLACK)
        self.renderer.draw_tournament_over(self.winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_MENU
                # ============================================================
# SECTION 6 — MAIN EXECUTION BLOCK
# ============================================================

if __name__ == "__main__":
    game = Game()
    game.run()