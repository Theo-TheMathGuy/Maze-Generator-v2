import pygame
from random import randint
class Area:
    def __init__(self, cell):
        self.cells = [cell]
        self.to_update = []
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.power = round(sum([c**2 for c in self.color])**.5, 4)/(3**.5)
    
    def set_color(self, color):
        self.color = color
        self.power = round(sum([c**2 for c in self.color])**.5, 4)/(3**.5)
    
    def absorb(self, area):
        self.to_update.extend(area.cells)
        self.cells.extend(area.cells)
    
    def display(self, screen, wall_color=(0, 0, 0), offset=(0, 0, 0)):
        for cell in self.cells:
            cell.display(screen, self.color, wall_color, offset)
    
    def display_update(self, screen, wall_color=(0, 0, 0), offset=(0, 0, 0)):
        for cell in self.to_update:
            cell.display(screen, self.color, wall_color, offset)