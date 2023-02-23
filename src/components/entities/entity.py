import pygame

from src.components.map import Map
from src.components.display_info import DisplayInfo

class Entity:
    def __init__(self):
        self.is_moving = False
        self.move_tick=0

    @staticmethod
    def click_event(entities_objects, events, display):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for entity in entities_objects:
                    if(entity.rect.collidepoint(pygame.mouse.get_pos())):
                        display.entity=entity
                        display.entity_save=entity
                        return
                display.entity=None
                return
    
    def attack(self,other):
        return(True)

    def move(self, map, coord,relative_coord, trace=True):
        self.is_moving = relative_coord
        if(trace):
            map.rm(self.map_pos)
        self.map_pos = coord
        if(trace):
            map.put(self.map_pos)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect) # Sprite draw

    def move_animation(self,map,player, entities_objects):
        if(self.is_moving):
            map.rect.topleft-=self.is_moving*3
            for entity in entities_objects:
                entity.rect.topleft-=self.is_moving*3
            if((self.rect.topleft[0]-map.rect.topleft[0])%48==0 and (self.rect.topleft[1]-map.rect.topleft[1])%48==0):# type: ignore                
                self.is_moving=False

        for entity in entities_objects:
            if(entity.move_tick==0):
                if(entity.is_moving):
                   entity.rect.topleft-=entity.is_moving*3
                   if((entity.rect.topleft[0]-player.rect.topleft[0])%48==0 and (entity.rect.topleft[1]-player.rect.topleft[1])%48==0 and not(self.is_moving)):# type: ignore                
                        entity.is_moving=False
            else:
                entity.move_tick-=1

    @staticmethod
    def play(map, entities_objects, player):
        for entity in entities_objects:
            if(map.can_attack(entity,player)):
                entity.attack(player)
            else:
                move=map.A_star(entity.map_pos, player.map_pos)
                if(not(move==[] or entity.map_pos == player.map_pos)):
                    entity.move(map, move[-1], entity.map_pos-move[-1])

    @staticmethod
    def check_if_moving(entities_objects):
        for entity in entities_objects:
            if(entity.is_moving):
                return(False)
        return(True)