import pygame

from src.services.visualization_service import VisualizationService
from src.components.map import Map
from src.components.entities.player import Player
from src.components.entities.entity import Entity
from src.components.UI.display_info import DisplayInfo
from src.global_state import GlobalState, PlayerStatus
from src.services.draw_service import draw_sprites
from src.components.UI.hotbar import Hotbar
from src.config import Config
from src.components.menu.menu import Menu

vec = pygame.math.Vector2

GlobalState.load_main_screen()
pygame.mouse.set_visible(False)

player = Player()
map = Map(player)
display = DisplayInfo()
hotbar = Hotbar()
damage_list = []
menu = Menu()

def main_menu_phase(events):
    menu.draw(GlobalState.SCREEN)

def gameplay_phase(events):
    player.move_animation(map, map.entities_objects)
    for i in range(len(map.entities_objects)):
        if(map.entities_objects[i].check_if_dead()):
            map.delete(i)
            break

    player.lost_game()
    if(GlobalState.PLAYER_STATE == PlayerStatus.MOVEMENT):
        player.move_input(map, map.entities_objects, damage_list)
        Entity.click_event(map.entities_objects, events, display)
        hotbar.click_event(events, player, map)
    
    elif(GlobalState.PLAYER_STATE == PlayerStatus.ATTACK):
        map.click_event(events, hotbar, damage_list)
        hotbar.click_event(events, player, map)

    elif(GlobalState.PLAYER_STATE == PlayerStatus.INVENTORY_MENU):
        pass

    player.inventory.events_handle(events)

    GlobalState.SCREEN.fill("black") # type: ignore
    map.draw(GlobalState.SCREEN)
    player.draw(GlobalState.SCREEN)
    draw_sprites(map.entities_objects)
    for i in range(len(damage_list)):
        damage_list[i].draw(GlobalState.SCREEN)
        if(damage_list[i].update()):
            damage_list.pop(i)
            break
    display.draw(GlobalState.SCREEN)
    hotbar.draw(GlobalState.SCREEN, player)
    player.inventory.draw(GlobalState.SCREEN, player)

def end_menu_phase(events):
    GlobalState.SCREEN.fill((71, 137, 216))
    GlobalState.SCREEN.blit(VisualizationService.get_main_font().render("PERDU",True,(0, 0, 0)), vec(Config.WIDTH/2, Config.HEIGHT/2))