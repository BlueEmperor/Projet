import pygame

from src.services.visualization_service import VisualizationService
from src.components.map import Map
from src.components.entities.player import Player
from src.components.entities.entity import Entity
from src.components.display_info import DisplayInfo
from src.global_state import GlobalState
from src.services.draw_service import draw_sprites
from src.components.entities.squelette import Squelette
from src.components.entities.vampire import Vampire

vec = pygame.math.Vector2

GlobalState.load_main_screen()

player = Player()
map = Map(player)
entities_objects = [Squelette(player.map_pos,vec(8,8), map),Vampire(player.map_pos,vec(12,2), map)]
display=DisplayInfo()

def main_menu_phase(events):
    pass

def gameplay_phase(events):
    player.update(map, entities_objects)
    Entity.click_event(entities_objects, events, display)
    GlobalState.SCREEN.fill("black") # type: ignore
    display.draw(GlobalState.SCREEN)
    map.draw(GlobalState.SCREEN)
    player.draw(GlobalState.SCREEN)
    draw_sprites(entities_objects)

def end_menu_phase(events):
    pass