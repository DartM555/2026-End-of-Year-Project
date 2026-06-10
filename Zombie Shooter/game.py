# Importing libraries
import json
import os
import random
import sys
import pygame

# starting pygame
pygame.init()

# game size
width,height, FPS = 800, 600, 60
# ground height
ground_height = height-60

# We define some colors to make it easier to change the color
black = (0,0,0)
white = (255,255,255)
red=(255,0,0)
green=(0,255,0)
dark_green=(20,255,40)
yellow=(255,215,0)
orange=(255,140,0)
light_gray=(180,180,180)
neon=(57,255,20)
SKY=(10,10,30)
SKY2=(30,10,60)

# high score file
HS_FILE = "highscore.json"

# Shop items
SHOP_ITEMS = [
    {"name": "Speed Boost", "description": "faster movement speed", "cost": 30, "key": "speed_boost"},
    {"name": "Shield", "description": "block a hit", "cost": 70, "key": "shield"},
    {"name": "Double Points", "description": "2x points for 10 seconds", "cost": 100, "key": "double_pts"}  
]
   
# creating the screen; setting the title and clock for frame rate
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zombie Dodge by Joshua D. and William Mejia")
clock = pygame.time.Clock()

# Setting font sizes (for title, score, etc.)
font_large = pygame.font.SysFont("Arial", 56, bold=True)
font_medium = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 22)
font_xsmall = pygame.font.SysFont("Arial", 17)


# ---- HELPER FUNCTIONS----


# loading high score from file
def load_high_score():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            return json.load(f)
    return []

# Saving the high score
def save_high_score(score):
    scores = load_high_score()
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:5]
    with open(HS_FILE, "w") as f:
        json.dump(scores, f)
    return scores

# function to draw text on screen
def draw_text(font, text, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x,y)
    else:
        rect.topleft = (x,y)
    screen.blit(surf, rect)
    
# function for background gradient
def bg():
    for y in range(height):
        t= y/height
        c=(
            int(SKY[0]+(SKY2[0]-SKY[0])* t), 
            int(SKY[1]+(SKY2[1]-SKY[1])* t),
            int(SKY[2]+(SKY2[2]-SKY[2])* t) 
           )
        pygame.draw.line(screen, c, (0,y), (width, y))
     
# function for the ground   
def ground():
    pygame.draw.rect(screen, dark_green, (0, ground_height, width, height-ground_height))
    pygame.draw.line(screen, green, (0, ground_height), (width, ground_height), 3)

# function for stars in the background
def stars(stars_list):
    for x,y in stars_list:
        pygame.draw.circle(screen, white, (x,y), 2)


# ---GAME CLASSES---
class Shop:
# Manages buying power-ups, tracking owned statuses, and handling
    def __init__(self):
        self.owned = {item["key"]: False for item in SHOP_ITEMS}
        self.time = {item["key"]: 0 for item in SHOP_ITEMS}


    def buy(self, key, cost, coins):
    # Deducts coins and gives ownership of an item if the player can afford it.
        if coins >= cost and key in self.owned:
            self.owned[key] = True
            return coins - cost
        return coins

    def use(self, key):
    # Consumes an owned powerup and activates its duration timers.
        if not self.owned.get(key, False):
            return 
        self.owned[key] = False
        
        if key == "speed_boost":
            self.time[key] = FPS * 8
        elif key == "double_pts":
            self.time[key] = FPS * 10
        elif key == "shield":
            self.time[key] = 1
        
    def tick(self):
        for k in self.time:
           if k != "shield" and self.time[k] > 0:
               self.time[k] -= 1
                
    def on(self, key):
        # Returns Ture if a powerup's timer is currently active
        return self.time[key] > 0
    
class Player:
    # Represents the player character, handling movement physics. screen boundaries, and drawing the chatracter's sprites.
    w = 36
    h = 52
    base = 5
    gravity = 0.6
    jump_power = -12
    
    def __init__(self,shop):
        self.shop = shop
        self.rect = pygame.Rect(width//2 - self.w // 2, ground_height - self.h, self.w, self.h)
        self.shield = False
        self.flash = 0 
        self.vy = 0
        self.is_jumping = False

    def speed(self):
        # Calculates the current movement speed, adding adjustments if Speed Boost is bought.
        speed = self.base
        if self.shop.on("speed_boost"):
            speed = int(speed * 1.8)
        return speed
            
    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed()
        self.rect.x = max(0, min(width - self.w, self.rect.x))
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not self.is_jumping:
            self.vy = self.jump_power
            self.is_jumping = True
            
        self.vy += self.gravity
        self.rect.y += int(self.vy)
        
        floor_level = ground_height - self.h
        if self.rect.y >= floor_level:
            self.rect.y = floor_level
            self.vy = 0
            self.is_jumping = False
        
        if self.flash > 0:
            self.flash -= 1     
            
    def draw(self, surf):  
        # base body
        body = red if self.flash > 0 else neon
        pygame.draw.rect(surf, body, (self.rect.x + 4, self.rect.y + 20, self.w - 8, self.h - 20), border_radius=8)

        # Head (Fixed typo from eclipse to ellipse, fixed coordinates and variables)
        pygame.draw.ellipse(surf, (240, 195, 145), (self.rect.x + 4, self.rect.y, self.w - 8, 22))
        
        # Eyes (Fixed period to comma, and fixed circle spelling)
        pygame.draw.circle(surf, black, (self.rect.x + 11, self.rect.y + 8), 3)
        pygame.draw.circle(surf, black, (self.rect.x + self.w - 11, self.rect.y + 8), 3)
        
        # Left and Right Feet (Fixed capitalized W and H variables)
        pygame.draw.rect(surf, (40, 60, 140), (self.rect.x + 4, self.rect.y + self.h - 12, 12, 12), border_radius=3)
        pygame.draw.rect(surf, (40, 60, 140), (self.rect.x + self.w - 16, self.rect.y + self.h - 12, 12, 12), border_radius=3)
        
        # Shield Bubble (if active - fixed capitalized W and H variables)
        if self.shield:
            pygame.draw.ellipse(surf, (100, 200, 255), (self.rect.x - 4, self.rect.y - 4, self.w + 8, self.h + 8), 3)
            
            
class Zombie:
    """Represents zombie enemies that can spawn falling from the sky
    or walking horizontally across the ground zone.
    """

    w = 32
    h = 46

    def __init__(self, speed, horizontal=False):
        self.horizontal = horizontal
        self.color = random.choice([(100, 180, 80), (80, 160, 60), (60, 140, 40)])
        y = random.randint(int(ground_height - self.h - 20), int(ground_height - self.h))

        if horizontal:
            # Configure ground-walking zombie coming from left or right margins
            side = random.choice(["left", "right"])
            y = random.randint(int(ground_height - self.h - 80), int(ground_height - self.h))
            if side == "left":
                self.rect = pygame.Rect(-self.w, y, self.w, self.h)
                self.vx = abs(speed)
            else:
                self.rect = pygame.Rect(width, y, self.w, self.h)
                self.vx = -abs(speed)
            self.vy = 0
        else:
            # Configure falling sky zombie
            x = random.randint(0, width - self.w)
            self.rect = pygame.Rect(x, -self.h, self.w, self.h)
            self.vy = speed
            self.vx = random.uniform(-1, 1)

    def update(self, slowmo=False):
        """Moves zombie positions. Cuts speed in half if Slow-Mo powerup is active."""
        f = 0.5 if slowmo else 1.0
        self.rect.x += int(self.vx * f)
        self.rect.y += int(self.vy * f)

    def off(self):
        """Checks if the zombie has completely moved off-screen boundaries."""
        if self.horizontal:
            return self.rect.right < 0 or self.rect.left > width
        return self.rect.top > height

    def draw(self, surf):
        """Draws the zombie sprite with green colors, glowing red eyes, and extended arms."""
        c = self.color
        # Torso & Head
        pygame.draw.rect(
            surf,
            c,
            (self.rect.x + 4, self.rect.y + 18, self.w - 8, self.h - 18),
            border_radius=4,
        )
        pygame.draw.ellipse(
            surf, c, (self.rect.x + 4, self.rect.y, self.w - 8, 20)
        )
        # Red eyes
        pygame.draw.circle(surf, red, (self.rect.x + 9, self.rect.y + 6), 3)
        pygame.draw.circle(
            surf, red, (self.rect.x + self.w - 9, self.rect.y + 6), 3
        )
        # Zombie arms stretched out forward
        pygame.draw.line(
            surf,
            c,
            (self.rect.x, self.rect.y + 24),
            (self.rect.x - 8, self.rect.y + 30),
            3,
        )
        pygame.draw.line(
            surf,
            c,
            (self.rect.right, self.rect.y + 24),
            (self.rect.right + 8, self.rect.y + 30),
            3,
        )
        # Feet
        pygame.draw.rect(
            surf,
            (40, 90, 30),
            (self.rect.x + 4, self.rect.bottom - 12, 10, 12),
            border_radius=2,
        )
        pygame.draw.rect(
            surf,
            (40, 90, 30),
            (self.rect.right - 14, self.rect.bottom - 12, 10, 12),
            border_radius=2,
        )

class Rock:
    """Represents hazard rocks that drop straight down from the sky."""

    def __init__(self, speed):
        self.w = random.randint(28, 50)
        self.h = random.randint(22, 40)
        self.rect = pygame.Rect(
            random.randint(0, width - self.w), -self.h, self.w, self.h
        )
        self.speed = speed

    def update(self, slowmo=False):
        """Drops the rock down. Affected by Slow-Mo state."""
        self.rect.y += int(self.speed * 0.5 if slowmo else self.speed)

    def off(self):
        """Returns True if the rock falls below screen limits."""
        return self.rect.top > height

    def draw(self, surf):
        """Draws a custom geometric gray rock polygon shape."""
        p = [
            (self.rect.x + self.w // 3, self.rect.y),
            (self.rect.right, self.rect.y + self.h // 3),
            (self.rect.right - 6, self.rect.bottom),
            (self.rect.x + 6, self.rect.bottom),
            (self.rect.x, self.rect.y + self.h // 2),
        ]
        pygame.draw.polygon(surf, light_gray, p)
        pygame.draw.polygon(surf, white, p, 2)


class Particle:
    """Represents visual burst particles generated when the player loses a life."""

    def __init__(self, x, y, color):
        self.x = x + random.randint(-10, 10)
        self.y = y + random.randint(-10, 10)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, -1)  # Burst upwards initially
        self.life = random.randint(20, 40)  # Total frame lifespan
        self.color = color
        self.size = random.randint(3, 7)

    def update(self):
        """Updates particle position physics, applying a gravity-like down pull."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravity acceleration effect
        self.life -= 1

    def draw(self, surf):
        """Draws individual circular particles."""
        pygame.draw.circle(
            surf, self.color, (int(self.x), int(self.y)), self.size
        )


# --- RENDER SCENE UI FUNCTIONS ---


def draw_menu(star_list):
    """Renders the main menu interface with titles, credits, and navigation options."""
    bg()
    stars(star_list)
    ground()
    draw_text(font_large, "Zombie Dodge", neon, width // 2, 100)
    draw_text(font_small, "by William Mejia & Joshua Dada", light_gray, width // 2, 168)

    items = [
        ("ENTER     - Start game", white),
        ("H         - High scores", yellow),
        ("S         - Shop", orange),
        ("ESC       - Quit", light_gray),
    ]
    for i, (txt, col) in enumerate(items):
        draw_text(font_medium, txt, col, width // 2, 260 + i * 50)
    draw_text(font_xsmall, "Use arrow keys or A / D to move", light_gray, width // 2, height - 30)


def draw_game_over(score, highscores, star_list):
    """Renders the Game Over screen presenting final stats and local top scores leaderboards."""
    bg()
    stars(star_list)
    draw_text(font_large, "GAME  OVER", red, width // 2, 90)
    draw_text(font_medium, f"Score: {score}", yellow, width // 2, 170)
    draw_text(font_medium, "Top Scores", orange, width // 2, 230)

    for i, s in enumerate(highscores[:5]):
        draw_text(
            font_small,
            f"  {i + 1}.  {s}",
            white,
            width // 2 - 80,
            270 + i * 34,
            center=False,
        )
    draw_text(font_medium, "ENTER - Restart    ESC - Menu", green, width // 2, height - 70)
   
def draw_highscores(highscores, star_list):
    bg()
    stars(star_list)
    draw_text(font_large, "HIGH SCORES", yellow, width // 2, 80)

    if not highscores:
        draw_text(font_medium, "No scores yet!", white, width // 2, 240)
    else:
        for i, s in enumerate(highscores[:5]):
            draw_text(font_small, f"  {i + 1}.     {s} pts", white, width // 2 - 120,170 + i * 52, center=False,  )

    draw_text(font_small, "ESC - Back", green, width // 2, height - 50)

def draw_shop_screen(shop, coins, star_list):
    
    text_blue = (0, 102, 204)
    bg()
    stars(star_list)
    draw_text(font_large, "SHOP", orange, width // 2, 40)
    draw_text(font_medium, f"Coins: {coins}", yellow, width // 2, 108)
    
    for i, item in enumerate(SHOP_ITEMS):
        x, y = 100, 170 + i * 110
        w_box, h_box = 600, 90
        owned = shop.owned[item["key"]]
        active = shop.on(item["key"])

        if active:
            bg_color = green
        elif owned:
            bg_color = light_gray
            status_txt = "Owned (Ready)"
        else:
            bg_color = white
            status_txt = f"Buy: {item['cost']} coins"
            
        pygame.draw.rect(screen, bg_color, (x, y, w_box, h_box), border_radius=10)
        pygame.draw.rect(screen, white, (x, y, w_box, h_box), 2, border_radius=10)
        
        box_center_x = x + (w_box // 2)
        
        draw_text(font_medium, f"{i+1}. {item['name']}", white, box_center_x, y + 22, center=True)
        draw_text(font_xsmall, item['description'], text_blue, box_center_x, y + 48, center=True)
        draw_text(font_medium, status_txt, yellow, box_center_x, y + 72, center=True)

    draw_text(font_small, "Press 1, 2, or 3 to Buy | ESC - Back to Menu", green, width // 2, height - 35)
    
def main():
    star_list = [(random.randint(0, width), random.randint(0, height - 80)) for _ in range(40)]
    state = "MENU"
    high_scores = load_high_score()
    total_coins = 0

    # Game variables
    player_shop = Shop()
    player = Player(player_shop)
    hazards = []
    particles = []
    score = 0
    lives = 3
    spawn_timer = 0

    while True:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if state == "MENU":
                    if event.key == pygame.K_RETURN:
                        player_shop = Shop()
                        player = Player(player_shop)
                        hazards, particles, score, lives, spawn_timer = [], [], 0, 3, 0
                        state = "GAME"
                    elif event.key == pygame.K_h:
                        high_scores = load_high_score()
                        state = "HIGHSCORES"
                    elif event.key == pygame.K_s:
                        state = "SHOP"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                elif state == "GAME":
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
                    elif event.key == pygame.K_1:
                        player_shop.use("speed_boost")
                    elif event.key == pygame.K_3:
                        player_shop.use("double_pts")
                        
                elif state == "SHOP":
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        idx = event.key - pygame.K_1
                        if idx < len(SHOP_ITEMS):
                            target = SHOP_ITEMS[idx]
                            total_coins = player_shop.buy(target["key"], target["cost"], total_coins)
                            if target["key"] == "shield" and player_shop.owned["shield"]:
                                player_shop.use("shield")
                                
                elif state == "HIGHSCORES" or state == "GAMEOVER":
                    if event.key == pygame.K_ESCAPE:
                        state = "MENU"
                    elif state == "GAMEOVER" and event.key == pygame.K_RETURN:
                        player_shop = Shop()
                        player = Player(player_shop)
                        hazards, particles, score, lives = [], [], 0, 3
                        state = "GAME"

        # State management routing
        if state == "MENU":
            draw_menu(star_list)
        elif state == "HIGHSCORES":
            draw_highscores(high_scores, star_list)
        elif state == "SHOP":
            draw_shop_screen(player_shop, total_coins, star_list)
        elif state == "GAMEOVER":
            draw_game_over(score, high_scores, star_list)
        elif state == "GAME":
            player_shop.tick()
            spawn_timer += 1
            
            points_gain = 2 if player_shop.on("double_pts") else 1
            score += points_gain
            
            if score % 100 == 0:
                total_coins += 5

            # Hazard spawning framework
            if spawn_timer % max(15, 45 - (score // 400)) == 0:
                speed_scale = 3 + (score // 1000)
                chosen = random.choice(["sky_zombie", "ground_zombie", "rock"])
                if chosen == "sky_zombie":
                    hazards.append(Zombie(speed=random.uniform(2, speed_scale), horizontal=False))
                elif chosen == "ground_zombie":
                    hazards.append(Zombie(speed=random.uniform(3, speed_scale + 1), horizontal=True))
                elif chosen == "rock":
                    hazards.append(Rock(speed=random.randint(4, speed_scale + 2)))

            player.update(keys)
            
            for h in hazards[:]:
                h.update()
                if h.off():
                    hazards.remove(h)
                    continue
                
                if player.rect.colliderect(h.rect):
                    player.flash = 15
                    for _ in range(12):
                        particles.append(Particle(player.rect.centerx, player.rect.centery, red))
                    hazards.remove(h)
                    
                    if player_shop.on("shield"):
                        player_shop.time["shield"] = 0 
                    else:
                        lives -= 1
                        if lives <= 0:
                            high_scores = save_high_score(score)
                            state = "GAMEOVER"

            for p in particles[:]:
                p.update()
                if p.life <= 0:
                    particles.remove(p)

            # Draw everything
            bg()
            stars(star_list)
            ground()
            for h in hazards: h.draw(screen)
            for p in particles: p.draw(screen)
            player.draw(screen)
            
            # HUD Display
            draw_text(font_small, f"Score: {score}", yellow, 20, 20, center=False)
            draw_text(font_small, f"Lives: {lives}", red, 20, 50, center=False)
            draw_text(font_small, f"Wallet: {total_coins} C", green, 20, 80, center=False)

        pygame.display.flip()

if __name__ == "__main__":
    main()    
    
    