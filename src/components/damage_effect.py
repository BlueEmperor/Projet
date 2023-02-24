import pygame

from src.services.visualization_service import VisualizationService
from src.config import Config
from math import cos, sin, pi
from random import random

vec = pygame.math.Vector2

class DamageEffect:
    def __init__(self, text, position):
        self.font = VisualizationService.get_main_font()
        self.text = text
        self.position = position
        self.velocity = random()+1
        self.angle = random()*2*pi/6+pi/3
        self.timer = Config.FPS + int(random()*Config.FPS)

    def draw(self, SCREEN):
        text = self.font.render(self.text,True, (255,255,255))
        text.set_alpha(255*self.timer/(2*Config.FPS))
        SCREEN.blit(text, self.position)

    def update(self):
        self.position+=vec(self.velocity*cos(self.angle),-self.velocity*sin(self.angle))
        self.timer-=1
        if(self.timer<=0):
            return(True)
        return(False)