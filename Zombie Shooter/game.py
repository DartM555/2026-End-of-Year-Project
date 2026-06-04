# Importing libraries
import pygame
import random
import json
import os
import sys

# starting pygame
pygame.init()

# game size
width,height = 800, 600
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
shop_items = [
    {"name": "Speed Boost", "description": "faster movement speed", "cost": 30, "key": "speed_boost"},
    {"name": "Shield", "description": "block a hit", "cost": 70, "key": "shield"},
    {"name": "Double Points", "description": "2x points for 10 seconds", "cost": 100, "key": "double_pts"}  
]
   
# creating the screen; setting the title and clock for frame rate
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("___________(not decided)")
clock = pygame.time.Clock()

# Setting font sizes (for title, score, etc.)
font_large = pygame.font.SysFont("Arial", 56, bold=True)
font_medium = pygame.font.SysFont("Arial", 32, bold=True)
font_small = pygame.font.SysFont("Arial", 22)
font_xsmall = pygame.font.SysFont("Arial", 17)

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
    scores.sorted(scores, reverse=True)[:5]
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
    screen.bilt(surf, rect)
    
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
