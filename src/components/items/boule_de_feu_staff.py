import pygame

from src.services.visualization_service import VisualizationService
from src.components.effects.lightning  import Lightning

class BdfStaff:
    def __init__(self):
        self.image = VisualizationService.get_staff_icon_image()
        self.rect = self.image.get_rect()
        self.range = (1,6)
        self.range_type = "linear"
        self.damage = 7
        self.type = "magic"
        self.animation = Lightning