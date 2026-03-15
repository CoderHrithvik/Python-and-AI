import pygame
import sys
from random import randint, choice

pygame.init()

# Window
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚽ Ultimate Football 2v2")

clock = pygame.time.Clock()
FONT_BIG = pygame.font.Font(None, 72)
FONT_MED = pygame.font.Font(None, 40)
FONT_SMALL = pygame.font.Font(None, 26)

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLUE = (50, 100, 220)
BLUE2 = (80, 150, 255)
RED = (200, 50, 50)
RED2 = (255, 120, 120)
YELLOW = (240, 220, 70)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)

WIN_TARGET = 2   # tournament: first to 2 wins

# Settings
settings = {
    "brightness": 1.0,          # 0.5–1.5
    "match_length": 90,         # seconds
    "powerups_enabled": True,
    "powerup_types": ["speed", "megashot", "shield", "freeze"],
}

# Team names (players choose)
team1_name = "Team Blue"
team2_name = "Team Red"

# Objects
player1 = pygame.Rect(200, HEIGHT // 2 - 25, 40, 40)              # Blue striker
player3 = pygame.Rect(160, HEIGHT // 2 + 60, 40, 40)              # Blue defender (4P)
player2 = pygame.Rect(WIDTH - 240, HEIGHT // 2 - 25, 40, 40)      # Red striker
player4 = pygame.Rect(WIDTH - 200, HEIGHT // 2 + 60, 40, 40)      # Red defender (4P)

gk_left = pygame.Rect(60, HEIGHT // 2 - 40, 25, 80)
gk_right = pygame.Rect(WIDTH - 85, HEIGHT // 2 - 40, 25, 80)

ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_vel = pygame.Vector2(4, 3)

goal_left = pygame.Rect(0, HEIGHT // 2 - 80, 20, 160)
goal_right = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 80, 20, 160)

pen_box_left = pygame.Rect(0, HEIGHT // 2 - 120, 140, 240)
pen_box_right = pygame.Rect(WIDTH - 140, HEIGHT // 2 - 120, 140, 240)

score_p1 = 0
score_p2 = 0
wins_p1 = 0
wins_p2 = 0

game_state = "menu"   # menu, settings, instructions, team_names, playing, penalty, gameover, tournament_over
mode = "pvp2"         # pvp2, pvp4, pvc
difficulty = "medium" # easy, medium, hard
start_ticks = 0

last_touch = None     # "p1" or "p2"
stamina_p1 = 100
stamina_p2 = 100
stamina_max = 100

anim_toggle = False
tournament_mode = False

powerups = []
powerup_timer = 0
pending_penalty_for = None  # "p1" or "p2"

# team name input
team_name_input_target = 1
team1_input = ""
team2_input = ""


def reset_positions(kickoff_to="p1"):
    global ball_vel, last_touch
    player1.x, player1.y = 200, HEIGHT // 2 - 25
    player3.x, player3.y = 160, HEIGHT // 2 + 60
    player2.x, player2.y = WIDTH - 240, HEIGHT // 2 - 25
    player4.x, player4.y = WIDTH - 200, HEIGHT // 2 + 60
    gk_left.x, gk_left.y = 60, HEIGHT // 2 - 40
    gk_right.x, gk_right.y = WIDTH - 85, HEIGHT // 2 - 40
    if kickoff_to == "p1":
        ball.center = (player1.centerx + 50, player1.centery)
        ball_vel.update(0, 0)
        last_touch = "p1"
    else:
        ball.center = (player2.centerx - 50, player2.centery)
        ball_vel.update(0, 0)
        last_touch = "p2"


def draw_field():
    brightness = settings["brightness"]
    color = (
        int(34 * brightness),
        int(139 * brightness),
        int(34 * brightness),
    )
    screen.fill(color)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 3)
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 90, 2)
    pygame.draw.rect(screen, WHITE, goal_left, 2)
    pygame.draw.rect(screen, WHITE, goal_right, 2)
    pygame.draw.rect(screen, WHITE, pen_box_left, 1)
    pygame.draw.rect(screen, WHITE, pen_box_right, 1)


def draw_objects():
    global anim_toggle
    p1_color = BLUE2 if anim_toggle else BLUE
    p3_color = BLUE2 if anim_toggle else BLUE
    p2_color = RED2 if anim_toggle else RED
    p4_color = RED2 if anim_toggle else RED
    pygame.draw.rect(screen, p1_color, player1)
    pygame.draw.rect(screen, p3_color, player3)
    pygame.draw.rect(screen, p2_color, player2)
    pygame.draw.rect(screen, p4_color, player4)
    pygame.draw.rect(screen, YELLOW, gk_left)
    pygame.draw.rect(screen, YELLOW, gk_right)
    pygame.draw.ellipse(screen, WHITE, ball)


def move_goalkeepers():
    if ball.centery < gk_left.centery and gk_left.top > 0:
        gk_left.y -= 3
    elif ball.centery > gk_left.centery and gk_left.bottom < HEIGHT:
        gk_left.y += 3

    if ball.centery < gk_right.centery and gk_right.top > 0:
        gk_right.y -= 3
    elif ball.centery > gk_right.centery and gk_right.bottom < HEIGHT:
        gk_right.y += 3


def handle_player_movement_pvp2(keys):
    global stamina_p1, stamina_p2, anim_toggle
    base_speed = 5
    sprint_bonus = 3
    anim_toggle = False

    # Player 1 (Blue striker)
    sprinting_p1 = keys[pygame.K_LSHIFT] and stamina_p1 > 0
    speed_p1 = base_speed + (sprint_bonus if sprinting_p1 else 0)
    if sprinting_p1:
        stamina_p1 = max(0, stamina_p1 - 0.5)
    else:
        stamina_p1 = min(stamina_max, stamina_p1 + 0.2)

    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= speed_p1
        anim_toggle = True
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += speed_p1
        anim_toggle = True
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= speed_p1
        anim_toggle = True
    if keys[pygame.K_d] and player1.right < WIDTH:
        player1.x += speed_p1
        anim_toggle = True

    # Player 2 (Red striker)
    sprinting_p2 = keys[pygame.K_RSHIFT] and stamina_p2 > 0
    speed_p2 = base_speed + (sprint_bonus if sprinting_p2 else 0)
    if sprinting_p2:
        stamina_p2 = max(0, stamina_p2 - 0.5)
    else:
        stamina_p2 = min(stamina_max, stamina_p2 + 0.2)

    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= speed_p2
        anim_toggle = True
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += speed_p2
        anim_toggle = True
    if keys[pygame.K_LEFT] and player2.left > 0:
        player2.x -= speed_p2
        anim_toggle = True
    if keys[pygame.K_RIGHT] and player2.right < WIDTH:
        player2.x += speed_p2
        anim_toggle = True


def handle_player_movement_pvp4(keys):
    global stamina_p1, stamina_p2, anim_toggle
    base_speed = 5
    sprint_bonus = 3
    anim_toggle = False

    # Player 1 (Blue striker) - WASD + LSHIFT
    sprinting_p1 = keys[pygame.K_LSHIFT] and stamina_p1 > 0
    speed_p1 = base_speed + (sprint_bonus if sprinting_p1 else 0)
    if sprinting_p1:
        stamina_p1 = max(0, stamina_p1 - 0.5)
    else:
        stamina_p1 = min(stamina_max, stamina_p1 + 0.2)

    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= speed_p1
        anim_toggle = True
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += speed_p1
        anim_toggle = True
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= speed_p1
        anim_toggle = True
    if keys[pygame.K_d] and player1.right < WIDTH:
        player1.x += speed_p1
        anim_toggle = True

    # Player 3 (Blue defender) - TFGH + Y
    if keys[pygame.K_y]:
        speed_p3 = base_speed + sprint_bonus
    else:
        speed_p3 = base_speed

    if keys[pygame.K_t] and player3.top > 0:
        player3.y -= speed_p3
        anim_toggle = True
    if keys[pygame.K_g] and player3.bottom < HEIGHT:
        player3.y += speed_p3
        anim_toggle = True
    if keys[pygame.K_f] and player3.left > 0:
        player3.x -= speed_p3
        anim_toggle = True
    if keys[pygame.K_h] and player3.right < WIDTH:
        player3.x += speed_p3
        anim_toggle = True

    # Player 2 (Red striker) - Arrows + RSHIFT
    sprinting_p2 = keys[pygame.K_RSHIFT] and stamina_p2 > 0
    speed_p2 = base_speed + (sprint_bonus if sprinting_p2 else 0)
    if sprinting_p2:
        stamina_p2 = max(0, stamina_p2 - 0.5)
    else:
        stamina_p2 = min(stamina_max, stamina_p2 + 0.2)

    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= speed_p2
        anim_toggle = True
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += speed_p2
        anim_toggle = True
    if keys[pygame.K_LEFT] and player2.left > 0:
        player2.x -= speed_p2
        anim_toggle = True
    if keys[pygame.K_RIGHT] and player2.right < WIDTH:
        player2.x += speed_p2
        anim_toggle = True

    # Player 4 (Red defender) - IJKL + O
    if keys[pygame.K_o]:
        speed_p4 = base_speed + sprint_bonus
    else:
        speed_p4 = base_speed

    if keys[pygame.K_i] and player4.top > 0:
        player4.y -= speed_p4
        anim_toggle = True
    if keys[pygame.K_k] and player4.bottom < HEIGHT:
        player4.y += speed_p4
        anim_toggle = True
    if keys[pygame.K_j] and player4.left > 0:
        player4.x -= speed_p4
        anim_toggle = True
    if keys[pygame.K_l] and player4.right < WIDTH:
        player4.x += speed_p4
        anim_toggle = True


def handle_player_movement_pvc(keys):
    global stamina_p1, stamina_p2, anim_toggle
    base_speed = 5
    sprint_bonus = 3
    anim_toggle = False

    if difficulty == "easy":
        ai_speed = 3
    elif difficulty == "hard":
        ai_speed = 6
    else:
        ai_speed = 4

    # Player 1 (human)
    sprinting_p1 = keys[pygame.K_LSHIFT] and stamina_p1 > 0
    speed_p1 = base_speed + (sprint_bonus if sprinting_p1 else 0)
    if sprinting_p1:
        stamina_p1 = max(0, stamina_p1 - 0.5)
    else:
        stamina_p1 = min(stamina_max, stamina_p1 + 0.2)

    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= speed_p1
        anim_toggle = True
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += speed_p1
        anim_toggle = True
    if keys[pygame.K_a] and player1.left > 0:
        player1.x -= speed_p1
        anim_toggle = True
    if keys[pygame.K_d] and player1.right < WIDTH:
        player1.x += speed_p1
        anim_toggle = True

    # Player 2 (AI striker)
    if ball.centery < player2.centery and player2.top > 0:
        player2.y -= ai_speed
    elif ball.centery > player2.centery and player2.bottom < HEIGHT:
        player2.y += ai_speed
    if ball.centerx < player2.centerx and player2.left > 0:
        player2.x -= ai_speed
    elif ball.centerx > player2.centerx and player2.right < WIDTH:
        player2.x += ai_speed

    # Player 4 (AI defender) simple follow ball on right half
    if ball.centery < player4.centery and player4.top > 0:
        player4.y -= ai_speed
    elif ball.centery > player4.centery and player4.bottom < HEIGHT:
        player4.y += ai_speed


def apply_power_shot(player_rect, direction):
    global ball_vel
    if player_rect.colliderect(ball):
        ball_vel = pygame.Vector2(direction * 12, randint(-6, 6))


def short_pass(player_rect):
    global ball_vel
    if player_rect.colliderect(ball):
        if player_rect.centerx < WIDTH // 2:
            ball_vel = pygame.Vector2(6, 0)
        else:
            ball_vel = pygame.Vector2(-6, 0)


def handle_collisions():
    global ball_vel, last_touch

    # --- Ceiling and floor bounce (anti-stuck version) ---
    if ball.top <= 0:
        ball.top = 0
        if abs(ball_vel.y) < 2:
            ball_vel.y = 3
        else:
            ball_vel.y *= -1

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        if abs(ball_vel.y) < 2:
            ball_vel.y = -3
        else:
            ball_vel.y *= -1

    # All outfield players
    for tag, p in (("p1", player1), ("p1", player3), ("p2", player2), ("p2", player4)):
        if p.colliderect(ball):
            dx = ball.centerx - p.centerx
            dy = ball.centery - p.centery
            v = pygame.Vector2(dx, dy)
            if v.length() == 0:
                v.update(1, 0)
            v = v.normalize() * 6
            ball_vel = v
            last_touch = tag

    for g in (gk_left, gk_right):
        if g.colliderect(ball):
            ball_vel.x *= -1.1
            ball_vel.y *= 1.05

def tackle(attacker, defender_tag):
    global ball_vel, last_touch, game_state, pending_penalty_for
    dist = attacker.centerx - ball.centerx, attacker.centery - ball.centery
    if abs(dist[0]) < 60 and abs(dist[1]) < 60:
        in_box = (defender_tag == "p2" and pen_box_right.colliderect(attacker)) or \
                 (defender_tag == "p1" and pen_box_left.colliderect(attacker))
        if in_box:
            pending_penalty_for = "p1" if defender_tag == "p2" else "p2"
            game_state = "penalty"
        else:
            ball_vel = pygame.Vector2(randint(-6, 6), randint(-6, 6))
            last_touch = None


def check_goals():
    global score_p1, score_p2
    if ball.colliderect(goal_right):
        score_p1 += 1
        reset_positions(kickoff_to="p2")
        return True
    if ball.colliderect(goal_left):
        score_p2 += 1
        reset_positions(kickoff_to="p1")
        return True
    return False


def check_out_of_bounds():
    if ball.right > WIDTH:
        if last_touch == "p1":
            ball.center = (WIDTH - 80, HEIGHT // 2)
            ball_vel.update(0, 0)
        else:
            y = goal_right.centery - 70 if ball.centery < HEIGHT // 2 else goal_right.centery + 70
            ball.center = (WIDTH - 40, y)
            ball_vel.update(-4, 0)
    elif ball.left < 0:
        if last_touch == "p2":
            ball.center = (80, HEIGHT // 2)
            ball_vel.update(0, 0)
        else:
            y = goal_left.centery - 70 if ball.centery < HEIGHT // 2 else goal_left.centery + 70
            ball.center = (40, y)
            ball_vel.update(4, 0)


def draw_score_and_timer():
    elapsed = max(0, settings["match_length"] - (pygame.time.get_ticks() - start_ticks) // 1000)
    score_text = FONT_MED.render(f"{team1_name} {score_p1}  -  {score_p2} {team2_name}", True, WHITE)
    time_text = FONT_MED.render(f"Time: {elapsed}", True, WHITE)
    wins_text = FONT_SMALL.render(f"Tournament: {team1_name} {wins_p1} - {wins_p2} {team2_name}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 50))
    screen.blit(wins_text, (WIDTH // 2 - wins_text.get_width() // 2, 80))
    return elapsed


def draw_stamina_bars():
    pygame.draw.rect(screen, GREY, (20, HEIGHT - 30, 200, 15))
    pygame.draw.rect(screen, BLUE, (20, HEIGHT - 30, 200 * (stamina_p1 / stamina_max), 15))
    txt1 = FONT_SMALL.render(f"{team1_name} Stamina", True, WHITE)
    screen.blit(txt1, (20, HEIGHT - 50))

    pygame.draw.rect(screen, GREY, (WIDTH - 220, HEIGHT - 30, 200, 15))
    pygame.draw.rect(screen, RED, (WIDTH - 220, HEIGHT - 30, 200 * (stamina_p2 / stamina_max), 15))
    txt2 = FONT_SMALL.render(f"{team2_name} Stamina", True, WHITE)
    screen.blit(txt2, (WIDTH - 220, HEIGHT - 50))


def draw_menu():
    screen.fill(GREEN)
    title = FONT_BIG.render("⚽ Ultimate Football 2v2", True, WHITE)
    m1 = FONT_MED.render("1: 2-Player (1 vs 1)", True, WHITE)
    m2 = FONT_MED.render("2: 4-Player (2 vs 2)", True, WHITE)
    m3 = FONT_MED.render("3: Tournament vs Computer", True, WHITE)
    m4 = FONT_MED.render("S: Settings", True, WHITE)
    m5 = FONT_MED.render("H: How to Play", True, WHITE)
    m6 = FONT_MED.render("N: Set Team Names", True, WHITE)
    d1 = FONT_SMALL.render("D: Difficulty Easy   F: Medium   G: Hard", True, WHITE)
    diff = FONT_SMALL.render(f"Current difficulty: {difficulty}", True, YELLOW)
    tn = FONT_SMALL.render(f"Teams: {team1_name} vs {team2_name}", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
    screen.blit(m1, (WIDTH // 2 - m1.get_width() // 2, 180))
    screen.blit(m2, (WIDTH // 2 - m2.get_width() // 2, 230))
    screen.blit(m3, (WIDTH // 2 - m3.get_width() // 2, 280))
    screen.blit(m4, (WIDTH // 2 - m4.get_width() // 2, 330))
    screen.blit(m5, (WIDTH // 2 - m5.get_width() // 2, 380))
    screen.blit(m6, (WIDTH // 2 - m6.get_width() // 2, 430))
    screen.blit(d1, (WIDTH // 2 - d1.get_width() // 2, 470))
    screen.blit(diff, (WIDTH // 2 - diff.get_width() // 2, 500))
    screen.blit(tn, (WIDTH // 2 - tn.get_width() // 2, 530))


def draw_settings_menu():
    screen.fill(GREEN)
    title = FONT_BIG.render("⚙ Settings", True, WHITE)
    b_text = FONT_MED.render(f"Brightness: {settings['brightness']:.1f}", True, WHITE)
    ml_text = FONT_MED.render(f"Match Length: {settings['match_length']}s", True, WHITE)
    pu_text = FONT_MED.render(f"Power-Ups: {'ON' if settings['powerups_enabled'] else 'OFF'}", True, WHITE)
    info = FONT_SMALL.render("LEFT/RIGHT: Brightness | UP/DOWN: Match time | P: Toggle power-ups | ENTER: Back", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(b_text, (WIDTH // 2 - b_text.get_width() // 2, 220))
    screen.blit(ml_text, (WIDTH // 2 - ml_text.get_width() // 2, 280))
    screen.blit(pu_text, (WIDTH // 2 - pu_text.get_width() // 2, 340))
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 420))


def draw_instructions():
    screen.fill(GREEN)
    title = FONT_BIG.render("📖 How to Play", True, WHITE)

    lines = [
        "Team Blue (Left):",
        "  Player 1 (Striker): Move W/A/S/D, Sprint LShift, Shoot Q, Pass E, Tackle F",
        "  Player 3 (Defender, 4P): Move T/F/G/H, Sprint Y, Shoot T, Pass R, Tackle V",
        "",
        "Team Red (Right):",
        "  Player 2 (Striker): Arrows, Sprint RShift, Shoot Right Ctrl, Pass /, Tackle Right Alt",
        "  Player 4 (Defender, 4P): Move I/J/K/L, Sprint O, Shoot I, Pass U, Tackle ;",
        "",
        "General:",
        "  Corners, goal kicks, penalties are automatic.",
        "  Power-ups appear on the pitch if enabled in Settings.",
        "  Tournament: first team to 2 match wins.",
        "  Press ENTER to return to the main menu.",
    ]

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    y = 140
    for line in lines:
        txt = FONT_SMALL.render(line, True, WHITE)
        screen.blit(txt, (40, y))
        y += 28


def draw_team_name_input():
    screen.fill(GREEN)
    title = FONT_BIG.render("Team Names", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    prompt1 = FONT_MED.render("Team 1 (Left / Blue):", True, WHITE)
    prompt2 = FONT_MED.render("Team 2 (Right / Red):", True, WHITE)
    input1 = FONT_MED.render(team1_input if team1_input else team1_name, True, YELLOW if team_name_input_target == 1 else WHITE)
    input2 = FONT_MED.render(team2_input if team2_input else team2_name, True, YELLOW if team_name_input_target == 2 else WHITE)
    info = FONT_SMALL.render("Type names, TAB to switch, ENTER to confirm.", True, WHITE)

    screen.blit(prompt1, (150, 200))
    screen.blit(input1, (150, 240))
    screen.blit(prompt2, (150, 320))
    screen.blit(input2, (150, 360))
    screen.blit(info, (150, 440))


def draw_gameover():
    screen.fill(GREEN)
    if score_p1 > score_p2:
        result = f"{team1_name} Wins the Match!"
    elif score_p2 > score_p1:
        result = f"{team2_name} Wins the Match!"
    else:
        result = "Draw!"
    title = FONT_BIG.render("Full Time!", True, WHITE)
    res_text = FONT_MED.render(result, True, WHITE)
    info = FONT_MED.render("Press ENTER for next match / menu", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))
    screen.blit(res_text, (WIDTH // 2 - res_text.get_width() // 2, 220))
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 300))


def draw_tournament_over():
    screen.fill(GREEN)
    if wins_p1 > wins_p2:
        result = f"{team1_name} Wins the Tournament!"
    else:
        result = f"{team2_name} Wins the Tournament!"
    title = FONT_BIG.render("Tournament Over!", True, WHITE)
    res_text = FONT_MED.render(result, True, YELLOW)
    info = FONT_MED.render("Press ENTER to return to menu", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))
    screen.blit(res_text, (WIDTH // 2 - res_text.get_width() // 2, 220))
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 300))


def setup_new_match():
    global score_p1, score_p2, start_ticks, stamina_p1, stamina_p2, powerups, powerup_timer
    score_p1 = score_p2 = 0
    stamina_p1 = stamina_p2 = 100
    powerups.clear()
    powerup_timer = 0
    reset_positions(kickoff_to=choice(["p1", "p2"]))
    start_ticks = pygame.time.get_ticks()


def spawn_powerup():
    if not settings["powerups_enabled"]:
        return
    p_type = choice(settings["powerup_types"])
    x = randint(150, WIDTH - 150)
    y = randint(80, HEIGHT - 80)
    rect = pygame.Rect(x, y, 30, 30)
    powerups.append({"type": p_type, "rect": rect})


def draw_powerups():
    for p in powerups:
        if p["type"] == "speed":
            pygame.draw.rect(screen, (0, 255, 0), p["rect"])
        elif p["type"] == "megashot":
            pygame.draw.rect(screen, (255, 0, 0), p["rect"])
        elif p["type"] == "shield":
            pygame.draw.rect(screen, (0, 200, 255), p["rect"])
        elif p["type"] == "freeze":
            pygame.draw.rect(screen, (150, 0, 255), p["rect"])


def apply_powerup(player, p_type):
    global stamina_p1, stamina_p2, ball_vel
    if p_type == "speed":
        if player == "p1":
            stamina_p1 = 100
        else:
            stamina_p2 = 100
    elif p_type == "megashot":
        ball_vel *= 1.8
    elif p_type == "shield":
        if player == "p1":
            player1.inflate_ip(10, 10)
            player3.inflate_ip(10, 10)
        else:
            player2.inflate_ip(10, 10)
            player4.inflate_ip(10, 10)
    elif p_type == "freeze":
        if player == "p1":
            player2.x, player2.y = player2.x, player2.y
            player4.x, player4.y = player4.x, player4.y
        else:
            player1.x, player1.y = player1.x, player1.y
            player3.x, player3.y = player3.x, player3.y


def check_powerup_collision():
    for p in powerups[:]:
        if player1.colliderect(p["rect"]) or player3.colliderect(p["rect"]):
            apply_powerup("p1", p["type"])
            powerups.remove(p)
        elif player2.colliderect(p["rect"]) or player4.colliderect(p["rect"]):
            apply_powerup("p2", p["type"])
            powerups.remove(p)


running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "pvp2"
                    tournament_mode = False
                    wins_p1 = wins_p2 = 0
                    setup_new_match()
                    game_state = "playing"
                elif event.key == pygame.K_2:
                    mode = "pvp4"
                    tournament_mode = False
                    wins_p1 = wins_p2 = 0
                    setup_new_match()
                    game_state = "playing"
                elif event.key == pygame.K_3:
                    mode = "pvc"
                    tournament_mode = True
                    wins_p1 = wins_p2 = 0
                    setup_new_match()
                    game_state = "playing"
                elif event.key == pygame.K_s:
                    game_state = "settings"
                elif event.key == pygame.K_h:
                    game_state = "instructions"
                elif event.key == pygame.K_n:
                    game_state = "team_names"
                elif event.key == pygame.K_d:
                    difficulty = "easy"
                elif event.key == pygame.K_f:
                    difficulty = "medium"
                elif event.key == pygame.K_g:
                    difficulty = "hard"

        elif game_state == "settings":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    settings["brightness"] = max(0.5, settings["brightness"] - 0.1)
                if event.key == pygame.K_RIGHT:
                    settings["brightness"] = min(1.5, settings["brightness"] + 0.1)
                if event.key == pygame.K_UP:
                    settings["match_length"] = min(300, settings["match_length"] + 10)
                if event.key == pygame.K_DOWN:
                    settings["match_length"] = max(30, settings["match_length"] - 10)
                if event.key == pygame.K_p:
                    settings["powerups_enabled"] = not settings["powerups_enabled"]
                if event.key == pygame.K_RETURN:
                    game_state = "menu"

        elif game_state == "instructions":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "menu"

        elif game_state == "team_names":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    team_name_input_target = 2 if team_name_input_target == 1 else 1
                elif event.key == pygame.K_RETURN:
                    if team1_input.strip():
                        team1_name = team1_input.strip()
                    if team2_input.strip():
                        team2_name = team2_input.strip()
                    game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    if team_name_input_target == 1:
                        team1_input = team1_input[:-1]
                    else:
                        team2_input = team2_input[:-1]
                else:
                    ch = event.unicode
                    if ch.isprintable():
                        if team_name_input_target == 1 and len(team1_input) < 16:
                            team1_input += ch
                        elif team_name_input_target == 2 and len(team2_input) < 16:
                            team2_input += ch

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                # Power shots
                if event.key == pygame.K_q:
                    apply_power_shot(player1, 1)
                if mode in ("pvp2", "pvp4") and event.key == pygame.K_RCTRL:
                    apply_power_shot(player2, -1)
                # Extra shots for defenders in 4P
                if mode == "pvp4":
                    if event.key == pygame.K_t:  # Blue defender shoot
                        apply_power_shot(player3, 1)
                    if event.key == pygame.K_i:  # Red defender shoot
                        apply_power_shot(player4, -1)

                # Passing
                if event.key == pygame.K_e:
                    short_pass(player1)
                if mode in ("pvp2", "pvp4") and event.key == pygame.K_SLASH:
                    short_pass(player2)
                if mode == "pvp4":
                    if event.key == pygame.K_r:
                        short_pass(player3)
                    if event.key == pygame.K_u:
                        short_pass(player4)

                # Tackling
                if event.key == pygame.K_f:
                    tackle(player1, "p2")
                if mode in ("pvp2", "pvp4") and event.key == pygame.K_RALT:
                    tackle(player2, "p1")
                if mode == "pvp4":
                    if event.key == pygame.K_v:
                        tackle(player3, "p2")
                    if event.key == pygame.K_SEMICOLON:
                        tackle(player4, "p1")

        elif game_state == "penalty":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if pending_penalty_for == "p1":
                    ball.center = (WIDTH - 200, HEIGHT // 2)
                    ball_vel.update(-10, randint(-3, 3))
                else:
                    ball.center = (200, HEIGHT // 2)
                    ball_vel.update(10, randint(-3, 3))
                game_state = "playing"

        elif game_state == "gameover":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if tournament_mode:
                    if wins_p1 >= WIN_TARGET or wins_p2 >= WIN_TARGET:
                        game_state = "tournament_over"
                    else:
                        setup_new_match()
                        game_state = "playing"
                else:
                    game_state = "menu"

        elif game_state == "tournament_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "menu"

    if game_state == "menu":
        draw_menu()

    elif game_state == "settings":
        draw_settings_menu()

    elif game_state == "instructions":
        draw_instructions()

    elif game_state == "team_names":
        draw_team_name_input()

    elif game_state == "playing":
        if mode == "pvp2":
            handle_player_movement_pvp2(keys)
        elif mode == "pvp4":
            handle_player_movement_pvp4(keys)
        else:
            handle_player_movement_pvc(keys)

        move_goalkeepers()

        ball.x += int(ball_vel.x)
        ball.y += int(ball_vel.y)

        handle_collisions()

        if not check_goals():
            check_out_of_bounds()

        powerup_timer += 1
        if powerup_timer > 600:
            spawn_powerup()
            powerup_timer = 0

        check_powerup_collision()

        draw_field()
        draw_objects()
        draw_powerups()
        remaining = draw_score_and_timer()
        draw_stamina_bars()

        if remaining <= 0:
            if score_p1 > score_p2:
                wins_p1 += 1
            elif score_p2 > score_p1:
                wins_p2 += 1
            game_state = "gameover"

    elif game_state == "penalty":
        draw_field()
        draw_objects()
        draw_powerups()
        draw_score_and_timer()
        draw_stamina_bars()
        msg = FONT_MED.render("PENALTY! Press SPACE to shoot.", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 120))

    elif game_state == "gameover":
        draw_gameover()

    elif game_state == "tournament_over":
        draw_tournament_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()