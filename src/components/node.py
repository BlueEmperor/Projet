import pygame

vec = pygame.math.Vector2

class Node:
    def __init__(self, coord, g_cost_before, end_coord, parent=None):
        self.g_cost=g_cost_before+1
        self.h_cost=pygame.math.Vector2.distance_to(end_coord,coord)
        self.total_cost=self.g_cost+self.h_cost
        self.parent=parent
        self.coord=coord
        self.end_coord=end_coord
    
    @staticmethod
    def lowest_node(list):
        Min_Node=list[0]
        for i in list:
            if(i.total_cost<Min_Node.total_cost):
                Min_Node=i
        return(Min_Node)
    
    @staticmethod
    def voisins(current):
        list=[]
        dir={pygame.K_z: vec(0,-1), pygame.K_s: vec(0,1), pygame.K_d: vec(1,0), pygame.K_q: vec(-1,0)}
        for i in dir.values():
            list.append(Node(i+current.coord,current.g_cost,current.end_coord,current))
        return(list)