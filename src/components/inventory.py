import pygame

from src.components.items.basic_sword import BasicSword
from src.components.items.basic_bow import BasicBow

class Inventory:
    def __init__(self):
        self.size=4
        self.items=[]
        self.in_hotbar=[BasicSword(),BasicBow()]
