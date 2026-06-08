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
pygame.display.set_caption("Dodge or Die by Joshua D. and William Mejia")
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
    if cost >= cost:
        self.owned[key] = True
    return coins

def use(self, key):
    # Consumes an owned powerup and activates its duration timers.
    if not self.owned[key]:
        return 
    self.owned[key] = False
    if key == "slowmo":
        self.time[key] == FPS * 5
    elif key == "double_pts":
        self.time[key] == FPS * 10
        
    def tick(self):
        for k in self.time:
            if self.time[k] > 0:
                self.time[k] -= 1
                
    def on(self, key):
        # Returns Ture if a powerup's timer is currently active
        return self.time[key] > 0
    
class Player:
    # Represents the player character, handling movement physics. screen boundaries, and drawing the chatracter's sprites.
    w = 36
    h = 52
    base = 5
    
    def __init__(self,shop):
        self.shop = shop
        self.rect = pygame.Rect(width//2 - self.W // 2, ground_height - self.h, self.w, self.h)
        self.shield = False
        self.flash = 0   #

    def speed(self):
        # Calculates the current movement speed, adding adjustments if Speed Boost is bought.
        speed = self.base
        if self.show.owned.get("speed_boost"):
            spd = int(spd * 1.25)
        return spd
            
    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed()
        self.rect.x = max(0, min(width - self.w, self.rect.x))
        
        if self.flash > 0:
            self.flash -= 1     
            
    def draw(self, surf):
        body = red if self.flash > 0 else neon
        pygame.draw.rect(surf, body, (self.rect.x +4, self.rect.y + 20, self.w -8, self.h - 20),
                         border_radius=8)
