import pygame
import random
import json
import sys


pygame.init()

width,height = 800, 600
g_y = height-60

black = (0,0,0)
white = (255,255,255)
red=(255,0,0)
green=(0,255,0)
dark_green=(20,255,40)
yellow=(255,215,0)
orange=(255,140,0)
light_gray=(180,180,180)
neon=(57,255,20)
sky=(10,10,30)

HS_FILE = "highscore.json"

shop_items = [
    {"name": "Speed Boost", "description": "faster movement speed", "cost": 30, "key": "speed_boost"}
    {"name": "Shield", "description": "block a hit", "cost": 70, "key": "shield"}
    {"name": "Double Points", "description": "2x points for 10 seconds", "cost": 100, "key": "double_pts"}  
]

screen = pygame.display.set_mode((width, height))