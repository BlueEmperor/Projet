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
        self.angle = random()*2*pi/6+pi/3
        rand=random()+2
        self.velocity = vec(rand*cos(self.angle),-rand*sin(self.angle))
        self.timer = Config.FPS + int(random()*Config.FPS)

    def draw(self, SCREEN):
        text = self.font.render(self.text,True, (255,255,255))
        text.set_alpha(255*self.timer/(2*Config.FPS))
        SCREEN.blit(text, self.position)

    def update(self):
        self.position+=self.velocity
        self.velocity[1]+=0.05
        self.timer-=1
        if(self.timer<=0):
            return(True)
        return(False)