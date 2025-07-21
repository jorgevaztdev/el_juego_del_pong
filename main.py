import pygame
import random
import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 192, 203)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "easy": {"ball_speed_x": 4, "ball_speed_y": 4},
    "medium": {"ball_speed_x": 6, "ball_speed_y": 6},
    "hard": {"ball_speed_x": 8, "ball_speed_y": 8},
}

# Paddle colors
PADDLE_COLORS = {
    "white": WHITE,
    "light_blue": LIGHT_BLUE,
    "light_red": LIGHT_RED,
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("El juego del ping pong")

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Scores
score_a = 0
score_b = 0
WINNING_SCORE = 5

# Font
font = pygame.font.Font(None, 74)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def save_score(winner, score_a, score_b):
    with open("/home/jorgevazt/Documents/Gemini/game_pong/scores.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Date: {timestamp}, Winner: {winner}, Score: {score_a} - {score_b}\n")

def intro_screen():
    intro = True
    player_side = None
    difficulty = "medium"
    paddle_color = WHITE

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    player_side = "left"
                    intro = False
                if event.key == pygame.K_r:
                    player_side = "right"
                    intro = False
                if event.key == pygame.K_1:
                    difficulty = "easy"
                if event.key == pygame.K_2:
                    difficulty = "medium"
                if event.key == pygame.K_3:
                    difficulty = "hard"
                if event.key == pygame.K_w:
                    paddle_color = WHITE
                if event.key == pygame.K_b:
                    paddle_color = LIGHT_BLUE
                if event.key == pygame.K_p:
                    paddle_color = LIGHT_RED

        screen.fill(BLACK)
        draw_text("El juego del ping pong", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10)
        instruction_font_large = pygame.font.Font(None, 45)
        instruction_font_small = pygame.font.Font(None, 35)

        rect_width = 650
        rect_height = 450 
        rect_x = (SCREEN_WIDTH - rect_width) // 2
        rect_y = (SCREEN_HEIGHT - rect_height) // 2 + 20

        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), 3)

        text_y_start = rect_y + 30 

        draw_text("Choose your side", instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start)
        draw_text("Press 'L' for Left Paddle", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 50)
        draw_text("Press 'R' for Right Paddle", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 85)

        draw_text("Difficulty: " + difficulty.upper(), instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 145)
        draw_text("1: Easy, 2: Medium, 3: Hard", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 180)

        draw_text("Paddle Color: ", instruction_font_large, paddle_color, screen, SCREEN_WIDTH // 2, text_y_start + 240)
        draw_text("W: White, B: Light Blue, P: Light Red", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 275)

        draw_text("Press 'Enter' to Pause", instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 335)
        draw_text("Press 'E' to Exit", instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 370)

        pygame.display.flip()
        pygame.time.Clock().tick(15)
    
    return player_side, difficulty, paddle_color

def pause_menu(current_difficulty, current_paddle_color):
    paused = True
    difficulty = current_difficulty
    paddle_color = current_paddle_color

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = False
                if event.key == pygame.K_1:
                    difficulty = "easy"
                if event.key == pygame.K_2:
                    difficulty = "medium"
                if event.key == pygame.K_3:
                    difficulty = "hard"
                if event.key == pygame.K_w:
                    paddle_color = WHITE
                if event.key == pygame.K_b:
                    paddle_color = LIGHT_BLUE
                if event.key == pygame.K_p:
                    paddle_color = LIGHT_RED

        screen.fill(BLACK)
        draw_text("The game has been paused", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        instruction_font_large = pygame.font.Font(None, 45)
        instruction_font_small = pygame.font.Font(None, 35)

        rect_width = 650
        rect_height = 300
        rect_x = (SCREEN_WIDTH - rect_width) // 2
        rect_y = (SCREEN_HEIGHT - rect_height) // 2 + 20

        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), 3)

        text_y_start = rect_y + 30

        draw_text("Difficulty: " + difficulty.upper(), instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start)
        draw_text("1: Easy, 2: Medium, 3: Hard", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 50)

        draw_text("Paddle Color: ", instruction_font_large, paddle_color, screen, SCREEN_WIDTH // 2, text_y_start + 110)
        draw_text("W: White, B: Light Blue, P: Light Red", instruction_font_small, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 160)

        draw_text("Press 'Enter' to Resume", instruction_font_large, WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 220)

        pygame.display.flip()
        pygame.time.Clock().tick(15)

    return difficulty, paddle_color

def main():
    global score_a, score_b

    player_side, difficulty, paddle_color = intro_screen()

    BALL_SPEED_X = DIFFICULTY_SETTINGS[difficulty]["ball_speed_x"]
    BALL_SPEED_Y = DIFFICULTY_SETTINGS[difficulty]["ball_speed_y"]

    paddle_a = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_b = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    paused = not paused
                    if paused:
                        difficulty, paddle_color = pause_menu(difficulty, paddle_color)
                        BALL_SPEED_X = DIFFICULTY_SETTINGS[difficulty]["ball_speed_x"]
                        BALL_SPEED_Y = DIFFICULTY_SETTINGS[difficulty]["ball_speed_y"]
                if event.key == pygame.K_e:
                    running = False

        if paused:
            continue

        keys = pygame.key.get_pressed()
        if player_side == "left":
            if keys[pygame.K_w] and paddle_a.top > 0:
                paddle_a.y -= PADDLE_SPEED
            if keys[pygame.K_s] and paddle_a.bottom < SCREEN_HEIGHT:
                paddle_a.y += PADDLE_SPEED
            # AI for paddle_b
            if paddle_b.centery < ball.centery:
                paddle_b.y += PADDLE_SPEED
            if paddle_b.centery > ball.centery:
                paddle_b.y -= PADDLE_SPEED
        else:
            if keys[pygame.K_UP] and paddle_b.top > 0:
                paddle_b.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and paddle_b.bottom < SCREEN_HEIGHT:
                paddle_b.y += PADDLE_SPEED
            # AI for paddle_a
            if paddle_a.centery < ball.centery:
                paddle_a.y += PADDLE_SPEED
            if paddle_a.centery > ball.centery:
                paddle_a.y -= PADDLE_SPEED


        # Prevent paddles from moving out of bounds
        if paddle_a.top < 0:
            paddle_a.top = 0
        if paddle_a.bottom > SCREEN_HEIGHT:
            paddle_a.bottom = SCREEN_HEIGHT
        if paddle_b.top < 0:
            paddle_b.top = 0
        if paddle_b.bottom > SCREEN_HEIGHT:
            paddle_b.bottom = SCREEN_HEIGHT

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
        
        if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
            ball_speed_x *= -1

        if ball.left <= 0:
            score_b += 1
            if score_b >= WINNING_SCORE:
                save_score("Player B", score_a, score_b)
                running = False
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))


        if ball.right >= SCREEN_WIDTH:
            score_a += 1
            if score_a >= WINNING_SCORE:
                save_score("Player A", score_a, score_b)
                running = False
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x *= random.choice((1, -1))
            ball_speed_y *= random.choice((1, -1))


        screen.fill(BLACK)
        pygame.draw.rect(screen, paddle_color, paddle_a)
        pygame.draw.rect(screen, paddle_color, paddle_b)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        draw_text(str(score_a), font, WHITE, screen, SCREEN_WIDTH // 4, 50)
        draw_text(str(score_b), font, WHITE, screen, SCREEN_WIDTH * 3 // 4, 50)

        pygame.display.flip()

        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
