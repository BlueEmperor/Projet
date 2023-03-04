import pygame

from src.services.visualization_service import VisualizationService
from src.config import Config
from src.components.node import Node
from src.components.entities.entity import Entity
from src.components.entities.squelette import Squelette
from src.components.entities.vampire import Vampire
from src.global_state import GlobalState
from src.components.status import PlayerStatus
from math import cos, sin, pi, floor

vec = pygame.math.Vector2

class Map(pygame.sprite.Sprite):
    ground="x"
    wall="w"
    dir={pygame.K_z: vec(0,-1), pygame.K_s: vec(0,1), pygame.K_d: vec(1,0), pygame.K_q: vec(-1,0)}
    
    def __init__(self,player):
        self.image = VisualizationService.get_map_image()
        self.rect = self.image.get_rect()
        self.tile_image = VisualizationService.get_tile_image()
        self.rect.topleft = vec(player.rect.topleft[0]-player.map_pos[0]*48,player.rect.topleft[1]-player.map_pos[1]*48) # type: ignore
        self._mat = [["w"]*16,["w"]+[self.ground]*3+["w"]*2+[self.ground]*4+["w"]*2+[self.ground]*3+["w"],["w"]+[self.ground]*14+["w"],["w"]+[self.ground]*3+["w"]*2+[self.ground]*4+["w"]*2+[self.ground]*3+["w"],["w"]*7+[self.ground]*2+["w"]*7,[" "]*5+["w"]*2+[self.ground]*2+["w"]*2+[" "]*5, [" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5,[" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5,[" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5, [" "]*5+["w"]*6+[" "]*5]
        self.player = player
        self.entities_objects = [Squelette(player.map_pos,vec(8,8), self),Vampire(player.map_pos,vec(12,2), self)]
        self.attack_tiles = []
        self.not_in_sight_tiles = []
        
    def __repr__(self):
        return("\n".join("".join(j for j in i) for i in self._mat)+"\n")
    
    def __contains__(self, coords):
        return(0<=int(coords[1])<len(self._mat) and 0<=int(coords[0])<len(self._mat[int(coords[1])]))
    
    def get_entity_by_coord(self, coords):
        for entity in self.entities_objects:
            if(entity.map_pos==coords):
                return(entity)
        return(None)
    
    def is_empty(self, coord):
        return(self._mat[int(coord[1])][int(coord[0])] == self.ground)
    
    def put(self, coord):
        self._mat[int(coord[1])][int(coord[0])]="e"
    
    def rm(self, coord):
        self._mat[int(coord[1])][int(coord[0])]=self.ground

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        for tile in self.attack_tiles:
            rect=pygame.Rect(self.player.rect.topleft+tile[0]*48+vec(3,3),(45,45))
            if(rect.collidepoint(pygame.mouse.get_pos())):
                color=(234, 207, 63)
            else:
                if(tile[1]):
                    color=(234, 74, 63)
                else:
                    color=(52, 179, 243)
            pygame.draw.rect(SCREEN, color, rect)

        for tile in self.not_in_sight_tiles:
            rect=pygame.Rect(self.player.rect.topleft+tile*48,(45,45))
            pygame.draw.rect(SCREEN, (135, 196, 226), rect)

    def can_attack(self, attaquant, cible):
        tile_list=self.create_tile_list(attaquant.weapon.range, attaquant)[0]
        for tile in tile_list:
            if(cible.map_pos==tile[0]+attaquant.map_pos):
                return(True)
        return(False)

    def A_star(self,start_coord,end_coord):
        open=[Node(start_coord,-1,end_coord)]
        close=[]
        current=open[0]
        while(True):
            if(len(open)==0):
                return([])
            
            current=Node.lowest_node(open)
            close.append(current)
            open.remove(current)
            if(current.coord==end_coord):
                break
            
            for voisin in Node.voisins(current):
                if(self._mat[int(voisin.coord[1])][int(voisin.coord[0])]==self.ground and not(voisin.coord in [i.coord for i in close])):
                    if(voisin.coord in [i.coord for i in open]):
                        a=[i.coord for i in open].index(voisin.coord)
                        if(open[a].total_cost>voisin.total_cost):
                            open[a]=voisin
                    else:
                        open.append(voisin)
        list=[]
        while(current.parent!=None):
            list.append(current.coord)
            current=current.parent
        return(list[1:])

    def create_tile_list(self, Range, entity):
        tile_list = []
        second_tile_list = []
        if(entity.weapon.range_type=="around"):
            for i in range(-Range[1],Range[1]+1):
                for j in range(-Range[1],Range[1]+1):
                    pos = vec(i,j)+entity.map_pos
                    if(Range[0]<=abs(i)+abs(j)<=Range[1] and pos in self and not(self._mat[int(pos[1])][int(pos[0])] in [self.wall, " "])):
                        if(self.line_of_sight(entity.map_pos,pos)):
                            tile_list.append([vec(i,j),self._mat[int(pos[1])][int(pos[0])]!=self.ground])
                        else:
                            second_tile_list.append(vec(i,j))
        
        elif(entity.weapon.range_type == "linear"):
            for i in range(4):
                for j in range(Range[0], Range[1]+1):
                    pos = vec(round(j*cos(pi/2*i)),round(j*sin(pi/2*i)))+entity.map_pos
                    if(pos in self and not(self._mat[int(pos[1])][int(pos[0])] in [self.wall, " "])):
                        if(self.line_of_sight(entity.map_pos,pos)):
                            tile_list.append([vec(round(j*cos(pi/2*i)),round(j*sin(pi/2*i))),self._mat[int(pos[1])][int(pos[0])]!=self.ground])
                        else:
                            second_tile_list.append(vec(j*cos(pi/2*i),j*sin(pi/2*i)))
                        
        return(tile_list, second_tile_list)

    def click_event(self, events, hotbar, damage_list):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for tile in self.attack_tiles:
                    if(tile[1]):
                        rect=pygame.Rect(self.player.rect.topleft+tile[0]*48,(45,45))
                        if(rect.collidepoint(pygame.mouse.get_pos())):
                            self.player.attack(self.get_entity_by_coord(tile[0]+self.player.map_pos), damage_list)
                            self.attack_tiles=[]
                            self.not_in_sight_tiles=[]
                            hotbar.selected=None
                            GlobalState.PLAYER_STATE = PlayerStatus.MOVEMENT
                            Entity.play(self, self.entities_objects, self.player, damage_list)
                            return
    
    def delete(self, i):
        pos=self.entities_objects[i].map_pos
        self._mat[int(pos[1])][int(pos[0])] = self.ground
        self.entities_objects.pop(i)
    
    def line_of_sight(self, coord1, coord2):
        List=[]
        corrected_x, corrected_y = 0, 0
        if(coord2[0]-coord1[0]<0):
            corrected_x = 1
        if(coord2[1]-coord1[1]<0):
            corrected_y = 1
        b=coord1[1]
        f=lambda x: slope*x + b
        if(coord1[0]-coord2[0]>0):
            sens=-1
        else:
            sens=1
        if(coord1[0]-coord2[0]!=0):
            slope=(coord1[1]-coord2[1])/(coord1[0]-coord2[0])
        if(corrected_x):
            for i in range(floor(coord1[0]),floor(coord2[0]),sens):
                b=coord1[1]+0.5-slope*(coord1[0]+0.5)
                List.append(vec(i-corrected_x,floor(f(i))))
                if(f(i)==floor(f(i))):
                    List.append(vec(i-corrected_x,floor(f(i))-1))
        else:
            for i in range(floor(coord1[0])+sens,floor(coord2[0])+sens,sens):
                slope=(coord1[1]-coord2[1])/(coord1[0]-coord2[0])
                b=coord1[1]+0.5-slope*(coord1[0]+0.5)
                List.append(vec(i,floor(f(i))))
                if(f(i)==floor(f(i))):
                    List.append(vec(i-1,floor(f(i))))
        f=lambda x: slope*(x-b)
        if(coord1[1]-coord2[1]>0):
            sens=-1
        else:
            sens=1
        if(coord1[1]-coord2[1]!=0):
            slope=(coord1[0]-coord2[0])/(coord1[1]-coord2[1])
        if(coord1[0]-coord2[0]==0):
            f=lambda x: coord1[0]
        if(corrected_y):
            for i in range(floor(coord1[1]),floor(coord2[1]),sens):
                List.append(vec(floor(f(i)),i-corrected_y))
                if(f(i)==floor(f(i)) and coord1[0]-coord2[0]!=0):
                    List.append(vec(floor(f(i))-1,i-corrected_y))
        else:
            for i in range(floor(coord1[1])+sens,floor(coord2[1])+sens,sens):
                List.append(vec(floor(f(i)),i))
                if(f(i)==floor(f(i))):
                    List.append(vec(floor(f(i)),i-1))
        for i in List:
            if(not(self._mat[int(i[1])][int(i[0])]==self.ground or i==coord2)):
                return(False)
        return(True)