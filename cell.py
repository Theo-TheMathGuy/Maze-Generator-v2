import pygame

class Cell:
    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.est = True
        self.sud = True
        self.cellSize = cellSize
        self.wallThickness = round(self.cellSize/5)

    def display(self, screen, color, wall_color=(0, 0, 0), offset=(0, 0)):
        cs, thickness = self.cellSize, self.wallThickness
        offsetX, offsetY = offset
        x, y = self.x*cs+offsetX, self.y*cs+offsetY
        pygame.draw.rect(screen, color, [x, y, cs, cs])
        if self.est:
            pygame.draw.rect(screen, wall_color, [x+cs-thickness, y, thickness, cs])
        if self.sud:
            pygame.draw.rect(screen, wall_color, [x, y+cs-thickness, cs, thickness])
        if not (self.sud or self.est):
            pygame.draw.rect(screen, wall_color, [x+cs-thickness, y+cs-thickness, thickness, thickness])
    
    def __eq__(self, cell):
        return cell.x == self.x and cell.y == self.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def is_in(self, collection):
        for cell in collection:
            if cell == self:
                return True
        return False