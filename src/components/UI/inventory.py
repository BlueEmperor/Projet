import pygame

from src.components.items.basic_sword import BasicSword
from src.components.items.basic_bow import BasicBow
from src.components.items.epic_sword import EpicSword
from src.components.items.boule_de_feu_staff import BdfStaff
from src.components.items.health_potion import HealthPotion
from src.global_state import GlobalState
from src.components.status import PlayerStatus
from src.config import Config
from src.services.visualization_service import VisualizationService

vec = pygame.math.Vector2

class Inventory:
    def __init__(self):
        self.size=18
        self.items=[BasicSword(),EpicSword(),HealthPotion(),BasicSword(),HealthPotion(),BasicBow(),BasicSword(),EpicSword(),BasicBow(),BasicSword(),EpicSword()]
        self.in_hotbar=[BasicSword(),BdfStaff(),BasicBow()]
        self.is_open=False
        self.offset=0
        self.WIDTH = 320
        self.HEIGHT = Config.HEIGHT-50
        self.speed=5
        self.offset = -self.WIDTH
        self.col = 4
        self.rect = pygame.Rect(self.offset,25,self.WIDTH,self.HEIGHT)
        self.alpha_screen = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        self.self_alpha_screen = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        self.item_on_cursor = None
        self.right_click = False
        self.font=VisualizationService.get_main_font()
        self.alpha=200
        self.buttons = [[], [self.use, self.destroy]]

    def draw(self, SCREEN, player):

        if(self.is_open):
            if(self.offset<25):
                self.offset+=self.speed
        else:
            if(self.offset>-self.WIDTH):
                self.offset-=self.speed
        
        self.alpha_screen.fill((0,0,0,0))
        self.rect=pygame.Rect(self.offset,25,self.WIDTH,self.HEIGHT)
        pygame.draw.rect(self.alpha_screen, (84,84,84, self.alpha), self.rect)
        self.alpha_screen.blit(self.font.render("Inventaire",True,(255, 255, 255)), (self.offset+125,50))
        self.alpha_screen.blit(player.image, vec(self.offset+25,50))

        for i in range(self.size//self.col):
            for j in range(int(self.col)):
                pygame.draw.rect(self.alpha_screen, (51, 51, 51, self.alpha), pygame.Rect(j*70+25+self.offset,120+i*70, 64, 64))
                if(len(self.items)>i*4+j):
                    self.items[i*4+j].rect.topleft=vec(j*70+25+self.offset,120+i*70)
                    self.alpha_screen.blit(self.items[i*4+j].image,vec(self.offset+j*70+25,120+i*70))
        
        for j in range(self.size%self.col):
            pygame.draw.rect(self.alpha_screen, (51, 51, 51, self.alpha), pygame.Rect(j*70+25+self.offset,120+self.size//self.col*70, 64, 64))
            if(len(self.items)>self.size//self.col*4+j):
                self.items[self.size//self.col*4+j].rect.topleft=vec(j*70+25+self.offset,120+self.size//self.col*70)
                self.alpha_screen.blit(self.items[self.size//self.col*4+j].image,vec(self.offset+j*70+25,120+self.size//self.col*70))

        if(self.item_on_cursor!=None and not(self.right_click)):
            self.self_alpha_screen.fill((0,0,0,0))
            pygame.draw.rect(self.self_alpha_screen , (200, 200, 200, 200), self.item_on_cursor.rect)
            SCREEN.blit(self.self_alpha_screen, (0,0))

        SCREEN.blit(self.alpha_screen, (0,0))

        if(self.item_on_cursor!=None and not(self.right_click)):
            rect=pygame.Rect(0,0,200,100)
            rect.topleft=(pygame.mouse.get_pos()[0]+30,pygame.mouse.get_pos()[1]-50)
            pygame.draw.rect(SCREEN, (30, 30, 30), rect)
            if(self.item_on_cursor.type == "potion"):
                SCREEN.blit(self.font.render("Usage : " + str(self.item_on_cursor.usage),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+10))
                SCREEN.blit(self.font.render("Heal : " + str(self.item_on_cursor.heal),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+40))
            else:
                SCREEN.blit(self.font.render("Damage : " + str(self.item_on_cursor.damage),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+10))
                SCREEN.blit(self.font.render("Portée : " + str(self.item_on_cursor.range),True,(255, 255, 255)), (rect.topleft[0]+10,rect.topleft[1]+40))
        
        elif(self.right_click):
            pygame.draw.rect(SCREEN, (30,30, 30), self.right_click[0])
            
            for button in self.buttons[0]:
                if(button.collidepoint(pygame.mouse.get_pos())):
                    self.self_alpha_screen.fill((0,0,0,0))
                    pygame.draw.rect(self.self_alpha_screen, (110, 110, 110, 160), button)
                    SCREEN.blit(self.self_alpha_screen, (0,0))
            if(len(self.buttons[0])==2):

                SCREEN.blit(self.font.render("Use",True,(255, 255, 255)), pygame.Rect((self.right_click[0].topleft[0]+5,self.right_click[0].topleft[1]+5), (80,80)))
                SCREEN.blit(self.font.render("Destroy",True,(255, 255, 255)), pygame.Rect((self.right_click[0].topleft[0]+5,self.right_click[0].topleft[1]+35), (80,80)))
            elif(len(self.buttons[0])==1):
                SCREEN.blit(self.font.render("Destroy",True,(255, 255, 255)), pygame.Rect((self.right_click[0].topleft[0]+5,self.right_click[0].topleft[1]+5), (80,80)))
                
    def destroy(self, item, player):
        self.items.pop(self.items.index(item))

    def use(self, item, entity):
        item.use(entity)
        self.items.pop(self.items.index(item))

    def events_handle(self, events, player):
        for event in events:
            if(self.buttons[0] != []):
                if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    for i in range(len(self.buttons[0])):
                        if(self.buttons[0][i].collidepoint(pygame.mouse.get_pos())):
                            self.buttons[1][i](self.right_click[1], player)
                            self.buttons[0] = []
                            self.right_click = None
                            return
                        
            if(event.type == pygame.MOUSEBUTTONDOWN):
                if(event.button == 3):
                    if(self.item_on_cursor != None):
                        if(self.item_on_cursor.type=="potion"):
                            self.right_click = [pygame.Rect(pygame.mouse.get_pos(), (110, 60)), self.item_on_cursor]
                            self.buttons[1]=[self.use, self.destroy]
                            self.buttons[0]=[pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+30*i, 110,30) for i in range(len(self.buttons[1]))]
                        else:
                            self.right_click = [pygame.Rect(pygame.mouse.get_pos(), (110, 30)), self.item_on_cursor]
                            self.buttons[1]=[self.destroy]
                            self.buttons[0]=[pygame.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+30*i, 110,30) for i in range(len(self.buttons[1]))]
                            
                    else:
                        self.right_click = None
                        self.buttons[0]=[]
                elif(event.button == 1 and self.right_click != None):
                    self.right_click = None
                    self.buttons[0]=[]

            elif(event.type == pygame.KEYDOWN and event.key == pygame.K_e):
                if(self.is_open):
                    self.is_open=False
                    GlobalState.PLAYER_STATE = PlayerStatus.MOVEMENT
                else:
                    self.is_open=True
                    GlobalState.PLAYER_STATE = PlayerStatus.INVENTORY_MENU
        
        for item in self.items:
            if(item.rect.collidepoint(pygame.mouse.get_pos())):
                self.item_on_cursor=item
                return


        self.item_on_cursor=None