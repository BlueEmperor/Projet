import pygame

from src.services.visualization_service import VisualizationService
from src.config import Config
from src.components.node import Node

vec = pygame.math.Vector2

class Map(pygame.sprite.Sprite):
    ground="x"
    wall="w"
    dir={pygame.K_z: vec(0,-1), pygame.K_s: vec(0,1), pygame.K_d: vec(1,0), pygame.K_q: vec(-1,0)}
    
    def __init__(self,player):
        self.image = VisualizationService.get_map_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(player.rect.topleft[0]-player.map_pos[0]*48,player.rect.topleft[1]-player.map_pos[1]*48) # type: ignore
        self._mat=[["w"]*16,["w"]+[self.ground]*3+["w"]*2+[self.ground]*4+["w"]*2+[self.ground]*3+["w"],["w"]+[self.ground]*14+["w"],["w"]+[self.ground]*3+["w"]*2+[self.ground]*4+["w"]*2+[self.ground]*3+["w"],["w"]*7+[self.ground]*2+["w"]*7,[" "]*5+["w"]*2+[self.ground]*2+["w"]*2+[" "]*5, [" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5,[" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5,[" "]*5+["w"]+[self.ground]*4+["w"]+[" "]*5, [" "]*5+["w"]*6+[" "]*5]

    def __repr__(self):
        return("\n".join("".join(j for j in i) for i in self._mat)+"\n")
    
    def is_empty(self, coord):
        if(self._mat[int(coord[1])][int(coord[0])] == "x"):
            return(True)
        return(False)
    
    def put(self, coord):
        self._mat[int(coord[1])][int(coord[0])]=self.wall
    
    def rm(self, coord):
        self._mat[int(coord[1])][int(coord[0])]=self.ground

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

    def can_attack(self, attaquant, cible):
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

    def get_map(self, entity_list):
        return()