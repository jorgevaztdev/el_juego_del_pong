import pygame
import random
import datetime
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Enhanced Color Palette
class Colors:
    # Background gradients
    BG_DARK = (15, 15, 25)
    BG_MID = (25, 25, 40)
    BG_LIGHT = (35, 35, 55)
    
    # Primary colors
    NEON_BLUE = (0, 150, 255)
    NEON_CYAN = (0, 255, 255)
    NEON_PURPLE = (150, 0, 255)
    NEON_PINK = (255, 0, 150)
    NEON_GREEN = (0, 255, 150)
    
    # Classic colors (enhanced)
    WHITE = (255, 255, 255)
    LIGHT_BLUE = (100, 200, 255)
    LIGHT_RED = (255, 100, 150)
    
    # Glow colors
    GLOW_BLUE = (50, 150, 255, 100)
    GLOW_CYAN = (50, 255, 255, 100)
    GLOW_PURPLE = (150, 50, 255, 100)
    GLOW_PINK = (255, 50, 150, 100)
    GLOW_WHITE = (255, 255, 255, 80)
    
    # UI colors
    UI_BORDER = (100, 100, 150)
    UI_BACKGROUND = (20, 20, 35, 180)
    TEXT_SHADOW = (0, 0, 0, 150)

# Visual themes
THEMES = {
    "neon": {
        "paddle_color": Colors.NEON_CYAN,
        "ball_color": Colors.NEON_PINK,
        "glow_color": Colors.GLOW_CYAN,
        "accent_color": Colors.NEON_PURPLE,
        "name": "Neon Cyberpunk"
    },
    "classic": {
        "paddle_color": Colors.WHITE,
        "ball_color": Colors.WHITE,
        "glow_color": Colors.GLOW_WHITE,
        "accent_color": Colors.LIGHT_BLUE,
        "name": "Classic Enhanced"
    },
    "ocean": {
        "paddle_color": Colors.LIGHT_BLUE,
        "ball_color": Colors.NEON_CYAN,
        "glow_color": Colors.GLOW_BLUE,
        "accent_color": Colors.NEON_BLUE,
        "name": "Ocean Depths"
    },
    "sunset": {
        "paddle_color": Colors.LIGHT_RED,
        "ball_color": Colors.NEON_PINK,
        "glow_color": Colors.GLOW_PINK,
        "accent_color": Colors.NEON_PURPLE,
        "name": "Sunset Glow"
    }
}

# Visual effects settings
class Effects:
    GLOW_RADIUS = 20
    PARTICLE_COUNT = 15
    SHAKE_INTENSITY = 5
    TRAIL_LENGTH = 8
    ANIMATION_SPEED = 0.1

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "easy": {"ball_speed_x": 4, "ball_speed_y": 4},
    "medium": {"ball_speed_x": 6, "ball_speed_y": 6},
    "hard": {"ball_speed_x": 8, "ball_speed_y": 8},
}

# Particle system
class Particle:
    def __init__(self, x, y, color, velocity_x=0, velocity_y=0):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x + random.uniform(-2, 2)
        self.velocity_y = velocity_y + random.uniform(-2, 2)
        self.life = 60  # frames
        self.max_life = 60
        self.size = random.uniform(2, 5)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life -= 1
        self.velocity_x *= 0.98  # friction
        self.velocity_y *= 0.98
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color_with_alpha = (*self.color[:3], alpha)
            current_size = self.size * (self.life / self.max_life)
            
            # Create a surface for the particle with alpha
            particle_surf = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color_with_alpha, 
                             (current_size, current_size), current_size)
            screen.blit(particle_surf, (self.x - current_size, self.y - current_size))

# Ball trail system
class BallTrail:
    def __init__(self):
        self.positions = []
        self.max_length = Effects.TRAIL_LENGTH
    
    def update(self, ball_x, ball_y):
        self.positions.append((ball_x, ball_y))
        if len(self.positions) > self.max_length:
            self.positions.pop(0)
    
    def draw(self, screen, color):
        for i, (x, y) in enumerate(self.positions):
            alpha = int(255 * (i / len(self.positions)) * 0.5)
            size = int(8 * (i / len(self.positions))) + 2
            
            trail_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            trail_color = (*color[:3], alpha)
            pygame.draw.circle(trail_surf, trail_color, (size, size), size)
            screen.blit(trail_surf, (x - size, y - size))

# Screen shake effect
class ScreenShake:
    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
    
    def add_shake(self, intensity, duration):
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)
    
    def update(self):
        if self.shake_duration > 0:
            self.shake_duration -= 1
            if self.shake_duration == 0:
                self.shake_intensity = 0
    
    def get_offset(self):
        if self.shake_intensity > 0:
            return (random.randint(-self.shake_intensity, self.shake_intensity),
                   random.randint(-self.shake_intensity, self.shake_intensity))
        return (0, 0)

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

# Enhanced Fonts
try:
    title_font = pygame.font.Font(None, 84)
    large_font = pygame.font.Font(None, 64)
    medium_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    score_font = pygame.font.Font(None, 96)
except:
    title_font = pygame.font.Font(None, 74)
    large_font = pygame.font.Font(None, 54)
    medium_font = pygame.font.Font(None, 38)
    small_font = pygame.font.Font(None, 28)
    score_font = pygame.font.Font(None, 86)

def draw_gradient_background(surface):
    """Draw a subtle gradient background"""
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(Colors.BG_DARK[0] + (Colors.BG_MID[0] - Colors.BG_DARK[0]) * ratio)
        g = int(Colors.BG_DARK[1] + (Colors.BG_MID[1] - Colors.BG_DARK[1]) * ratio)
        b = int(Colors.BG_DARK[2] + (Colors.BG_MID[2] - Colors.BG_DARK[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

def draw_glow_circle(surface, color, center, radius, glow_radius=20):
    """Draw a circle with glow effect"""
    # Draw multiple circles with decreasing alpha for glow effect
    for i in range(glow_radius, 0, -2):
        alpha = int(30 * (glow_radius - i) / glow_radius)
        glow_surf = pygame.Surface((i * 2, i * 2), pygame.SRCALPHA)
        glow_color = (*color[:3], alpha)
        pygame.draw.circle(glow_surf, glow_color, (i, i), i)
        surface.blit(glow_surf, (center[0] - i, center[1] - i))
    
    # Draw the main circle
    pygame.draw.circle(surface, color, center, radius)

def draw_glow_rect(surface, color, rect, glow_radius=10, corner_radius=8):
    """Draw a rounded rectangle with glow effect"""
    # Draw glow effect
    for i in range(glow_radius, 0, -1):
        alpha = int(40 * (glow_radius - i) / glow_radius)
        glow_surf = pygame.Surface((rect.width + i * 2, rect.height + i * 2), pygame.SRCALPHA)
        glow_color = (*color[:3], alpha)
        glow_rect = pygame.Rect(i, i, rect.width, rect.height)
        pygame.draw.rect(glow_surf, glow_color, glow_rect, border_radius=corner_radius + i)
        surface.blit(glow_surf, (rect.x - i, rect.y - i))
    
    # Draw the main rectangle
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_text_with_shadow(text, font, color, surface, x, y, shadow_offset=2):
    """Draw text with shadow effect"""
    # Draw shadow
    shadow_text = font.render(text, True, Colors.TEXT_SHADOW[:3])
    shadow_rect = shadow_text.get_rect()
    shadow_rect.center = (x + shadow_offset, y + shadow_offset)
    surface.blit(shadow_text, shadow_rect)
    
    # Draw main text
    main_text = font.render(text, True, color)
    main_rect = main_text.get_rect()
    main_rect.center = (x, y)
    surface.blit(main_text, main_rect)

def draw_animated_center_line(surface, color, time_offset=0):
    """Draw an animated center line with glowing dots"""
    dot_spacing = 20
    dot_radius = 3
    num_dots = SCREEN_HEIGHT // dot_spacing
    
    for i in range(num_dots):
        y = i * dot_spacing + 10
        # Animate the glow intensity
        glow_intensity = (math.sin(time_offset + i * 0.3) + 1) * 0.5
        current_color = [int(c * (0.5 + glow_intensity * 0.5)) for c in color[:3]]
        
        # Draw glowing dot
        for radius in range(8, 0, -1):
            alpha = int(60 * (8 - radius) / 8 * glow_intensity)
            dot_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            dot_color = (*current_color, alpha)
            pygame.draw.circle(dot_surf, dot_color, (radius, radius), radius)
            surface.blit(dot_surf, (SCREEN_WIDTH // 2 - radius, y - radius))
        
        # Main dot
        pygame.draw.circle(surface, current_color, (SCREEN_WIDTH // 2, y), dot_radius)

def draw_modern_ui_box(surface, rect, border_color, bg_color, corner_radius=15):
    """Draw a modern UI box with rounded corners and transparency"""
    # Create surface with alpha
    box_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    # Draw background with transparency
    pygame.draw.rect(box_surf, bg_color, (0, 0, rect.width, rect.height), border_radius=corner_radius)
    
    # Draw border
    pygame.draw.rect(box_surf, border_color, (0, 0, rect.width, rect.height), 3, border_radius=corner_radius)
    
    surface.blit(box_surf, rect.topleft)

def save_score(winner, score_a, score_b):
    with open("scores.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Date: {timestamp}, Winner: {winner}, Score: {score_a} - {score_b}\n")

def intro_screen():
    intro = True
    player_side = None
    difficulty = "medium"
    current_theme = "neon"
    animation_time = 0

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
                if event.key == pygame.K_n:
                    current_theme = "neon"
                if event.key == pygame.K_c:
                    current_theme = "classic"
                if event.key == pygame.K_o:
                    current_theme = "ocean"
                if event.key == pygame.K_s:
                    current_theme = "sunset"

        # Draw gradient background
        draw_gradient_background(screen)
        
        # Animated title with glow
        title_glow_intensity = (math.sin(animation_time * 0.05) + 1) * 0.3 + 0.7
        title_color = [int(c * title_glow_intensity) for c in THEMES[current_theme]["accent_color"][:3]]
        draw_text_with_shadow("El Juego del Ping Pong", title_font, title_color, 
                            screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8, 3)

        # Modern UI box
        rect_width = 700
        rect_height = 480
        rect_x = (SCREEN_WIDTH - rect_width) // 2
        rect_y = (SCREEN_HEIGHT - rect_height) // 2 + 40
        ui_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        
        draw_modern_ui_box(screen, ui_rect, Colors.UI_BORDER, Colors.UI_BACKGROUND)

        text_y_start = rect_y + 40
        theme_color = THEMES[current_theme]["accent_color"]

        # Side selection
        draw_text_with_shadow("Choose Your Side", medium_font, Colors.WHITE, 
                            screen, SCREEN_WIDTH // 2, text_y_start)
        draw_text_with_shadow("Press 'L' for Left Paddle  |  Press 'R' for Right Paddle", 
                            small_font, theme_color, screen, SCREEN_WIDTH // 2, text_y_start + 40)

        # Difficulty selection
        diff_color = THEMES[current_theme]["paddle_color"]
        draw_text_with_shadow(f"Difficulty: {difficulty.upper()}", medium_font, diff_color, 
                            screen, SCREEN_WIDTH // 2, text_y_start + 100)
        draw_text_with_shadow("1: Easy  |  2: Medium  |  3: Hard", small_font, Colors.WHITE, 
                            screen, SCREEN_WIDTH // 2, text_y_start + 140)

        # Theme selection
        draw_text_with_shadow(f"Theme: {THEMES[current_theme]['name']}", medium_font, 
                            THEMES[current_theme]["ball_color"], screen, SCREEN_WIDTH // 2, text_y_start + 200)
        draw_text_with_shadow("N: Neon  |  C: Classic  |  O: Ocean  |  S: Sunset", 
                            small_font, Colors.WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 240)

        # Preview paddles with current theme
        preview_paddle_left = pygame.Rect(SCREEN_WIDTH // 2 - 100, text_y_start + 280, 15, 60)
        preview_paddle_right = pygame.Rect(SCREEN_WIDTH // 2 + 85, text_y_start + 280, 15, 60)
        draw_glow_rect(screen, THEMES[current_theme]["paddle_color"], preview_paddle_left, 8, 8)
        draw_glow_rect(screen, THEMES[current_theme]["paddle_color"], preview_paddle_right, 8, 8)
        
        # Preview ball
        ball_center = (SCREEN_WIDTH // 2, text_y_start + 310)
        draw_glow_circle(screen, THEMES[current_theme]["ball_color"], ball_center, 8, 15)

        # Controls
        draw_text_with_shadow("Press 'Enter' to Pause  |  Press 'E' to Exit", 
                            small_font, Colors.LIGHT_BLUE, screen, SCREEN_WIDTH // 2, text_y_start + 380)

        animation_time += 1
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    
    return player_side, difficulty, current_theme

def pause_menu(current_difficulty, current_theme):
    paused = True
    difficulty = current_difficulty
    theme = current_theme
    animation_time = 0

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
                if event.key == pygame.K_n:
                    theme = "neon"
                if event.key == pygame.K_c:
                    theme = "classic"
                if event.key == pygame.K_o:
                    theme = "ocean"
                if event.key == pygame.K_s:
                    theme = "sunset"

        # Draw gradient background
        draw_gradient_background(screen)
        
        # Animated pause title
        pause_glow_intensity = (math.sin(animation_time * 0.08) + 1) * 0.3 + 0.7
        pause_color = [int(c * pause_glow_intensity) for c in THEMES[theme]["accent_color"][:3]]
        draw_text_with_shadow("GAME PAUSED", large_font, pause_color, 
                            screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, 3)

        # Modern UI box
        rect_width = 600
        rect_height = 320
        rect_x = (SCREEN_WIDTH - rect_width) // 2
        rect_y = (SCREEN_HEIGHT - rect_height) // 2 + 20
        ui_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        
        draw_modern_ui_box(screen, ui_rect, Colors.UI_BORDER, Colors.UI_BACKGROUND)

        text_y_start = rect_y + 40

        # Difficulty selection
        diff_color = THEMES[theme]["paddle_color"]
        draw_text_with_shadow(f"Difficulty: {difficulty.upper()}", medium_font, diff_color, 
                            screen, SCREEN_WIDTH // 2, text_y_start)
        draw_text_with_shadow("1: Easy  |  2: Medium  |  3: Hard", small_font, Colors.WHITE, 
                            screen, SCREEN_WIDTH // 2, text_y_start + 40)

        # Theme selection
        draw_text_with_shadow(f"Theme: {THEMES[theme]['name']}", medium_font, 
                            THEMES[theme]["ball_color"], screen, SCREEN_WIDTH // 2, text_y_start + 100)
        draw_text_with_shadow("N: Neon  |  C: Classic  |  O: Ocean  |  S: Sunset", 
                            small_font, Colors.WHITE, screen, SCREEN_WIDTH // 2, text_y_start + 140)

        # Resume instruction with pulsing effect
        resume_intensity = (math.sin(animation_time * 0.1) + 1) * 0.3 + 0.7
        resume_color = [int(c * resume_intensity) for c in Colors.NEON_GREEN[:3]]
        draw_text_with_shadow("Press 'Enter' to Resume", medium_font, resume_color, 
                            screen, SCREEN_WIDTH // 2, text_y_start + 220)

        animation_time += 1
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return difficulty, theme

def main():
    global score_a, score_b

    player_side, difficulty, current_theme = intro_screen()

    BALL_SPEED_X = DIFFICULTY_SETTINGS[difficulty]["ball_speed_x"]
    BALL_SPEED_Y = DIFFICULTY_SETTINGS[difficulty]["ball_speed_y"]

    paddle_a = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_b = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

    # Initialize visual effects
    particles = []
    ball_trail = BallTrail()
    screen_shake = ScreenShake()
    animation_time = 0
    score_animation_a = 0
    score_animation_b = 0

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
                        difficulty, current_theme = pause_menu(difficulty, current_theme)
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

        # Ball collision with top/bottom walls
        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1
            # Add particles for wall collision
            for _ in range(5):
                particles.append(Particle(ball.centerx, ball.centery, 
                                        THEMES[current_theme]["ball_color"], 
                                        ball_speed_x * 0.3, ball_speed_y * -0.5))
        
        # Ball collision with paddles
        if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
            ball_speed_x *= -1
            # Add screen shake and particles
            screen_shake.add_shake(Effects.SHAKE_INTENSITY, 10)
            for _ in range(Effects.PARTICLE_COUNT):
                particles.append(Particle(ball.centerx, ball.centery, 
                                        THEMES[current_theme]["paddle_color"], 
                                        ball_speed_x * 0.2, random.uniform(-3, 3)))

        # Scoring
        if ball.left <= 0:
            score_b += 1
            score_animation_b = 30  # Animation frames
            # Score particles
            for _ in range(20):
                particles.append(Particle(ball.centerx, ball.centery, 
                                        THEMES[current_theme]["accent_color"], 
                                        random.uniform(-5, 5), random.uniform(-5, 5)))
            if score_b >= WINNING_SCORE:
                save_score("Player B", score_a, score_b)
                running = False
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
            ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

        if ball.right >= SCREEN_WIDTH:
            score_a += 1
            score_animation_a = 30  # Animation frames
            # Score particles
            for _ in range(20):
                particles.append(Particle(ball.centerx, ball.centery, 
                                        THEMES[current_theme]["accent_color"], 
                                        random.uniform(-5, 5), random.uniform(-5, 5)))
            if score_a >= WINNING_SCORE:
                save_score("Player A", score_a, score_b)
                running = False
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
            ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))


        # Update visual effects
        ball_trail.update(ball.centerx, ball.centery)
        screen_shake.update()
        
        # Update particles
        particles = [p for p in particles if p.life > 0]
        for particle in particles:
            particle.update()
        
        # Update score animations
        if score_animation_a > 0:
            score_animation_a -= 1
        if score_animation_b > 0:
            score_animation_b -= 1

        # Get screen shake offset
        shake_x, shake_y = screen_shake.get_offset()
        
        # Draw gradient background
        draw_gradient_background(screen)
        
        # Draw animated center line
        draw_animated_center_line(screen, THEMES[current_theme]["accent_color"], animation_time * 0.1)
        
        # Draw ball trail
        ball_trail.draw(screen, THEMES[current_theme]["ball_color"])
        
        # Draw paddles with glow effect
        paddle_a_offset = pygame.Rect(paddle_a.x + shake_x, paddle_a.y + shake_y, 
                                     paddle_a.width, paddle_a.height)
        paddle_b_offset = pygame.Rect(paddle_b.x + shake_x, paddle_b.y + shake_y, 
                                     paddle_b.width, paddle_b.height)
        
        draw_glow_rect(screen, THEMES[current_theme]["paddle_color"], paddle_a_offset, 12, 8)
        draw_glow_rect(screen, THEMES[current_theme]["paddle_color"], paddle_b_offset, 12, 8)
        
        # Draw ball with glow effect
        ball_center = (ball.centerx + shake_x, ball.centery + shake_y)
        draw_glow_circle(screen, THEMES[current_theme]["ball_color"], ball_center, BALL_SIZE // 2, 20)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw scores with animation
        score_a_scale = 1.0 + (score_animation_a / 30.0) * 0.3
        score_b_scale = 1.0 + (score_animation_b / 30.0) * 0.3
        
        # Score A
        score_a_color = THEMES[current_theme]["paddle_color"] if score_animation_a > 0 else Colors.WHITE
        score_a_font = pygame.font.Font(None, int(96 * score_a_scale))
        draw_text_with_shadow(str(score_a), score_a_font, score_a_color, 
                            screen, SCREEN_WIDTH // 4 + shake_x, 60 + shake_y, 3)
        
        # Score B
        score_b_color = THEMES[current_theme]["paddle_color"] if score_animation_b > 0 else Colors.WHITE
        score_b_font = pygame.font.Font(None, int(96 * score_b_scale))
        draw_text_with_shadow(str(score_b), score_b_font, score_b_color, 
                            screen, SCREEN_WIDTH * 3 // 4 + shake_x, 60 + shake_y, 3)

        animation_time += 1
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
