import pygame
from cell import Cell
from area import Area
from random import choice, random
from os import environ as env

class Maze:
    def __init__(self, dim, cellSize, screen):
        self.seed = round(random()*100_000)
        self.screen = screen
        offset = round(cellSize/10)
        self.offset = (offset, offset)

        self.dim = dim
        self.cellSize = cellSize
        self.cells = []
        for y in range(self.dim[1]):
            for x in range(self.dim[0]):
                self.cells.append(Cell(x, y, self.cellSize))
        self.areas = [Area(cell) for cell in self.cells]
        self.to_update = [area for area in self.areas]
        self.areas[0].set_color((255, 255, 255))

        self.pause = True
        self.is_ready = False
        self.is_solving = False
        self.is_solved = False

        self.start = self.cells[0]
        self.end = self.cells[-1]
        self.solution = [self.start]
        self.visited = []

        self.queue = [(self.start, -1)]
        self.next_queue = []

        self.display()
    
    def get_cell(self, x, y):
        for cell in self.cells:
            if cell.x==x and cell.y==y:
                return cell
        return None

    def get_area_of_cell(self, cell):
        for area in self.areas:
            if cell in area.cells:
                return area
        return None

    def check_adj(self, x, y):
        possible = []
        current = self.get_cell(x, y)
        if current.x != 0:
            left = self.get_cell(x-1, y)
            if left.est: possible.append(left)
        if current.x != self.dim[0]-1:
            right = self.get_cell(x+1, y)
            if current.est: possible.append(right)
        if current.y != 0:
            up = self.get_cell(x, y-1)
            if up.sud: possible.append(up)
        if current.y != self.dim[1]-1:
            down = self.get_cell(x, y+1)
            if current.sud: possible.append(down)
        return possible

    def get_joinable(self, x, y):
        current = self.get_cell(x, y)
        left = self.get_cell(x-1, y)
        right = self.get_cell(x+1, y)
        up = self.get_cell(x, y-1)
        down = self.get_cell(x, y+1)
        joinable = []
        if left is not None:
            if not left.est: joinable.append(left)
        if right is not None:
            if not current.est: joinable.append(right)
        if up is not None:
            if not up.sud: joinable.append(up)
        if down is not None:
            if not current.sud: joinable.append(down)
        return joinable
    
    def display(self):
        screen = self.screen
        border_thickness = round(self.cellSize/10)
        offset = (border_thickness, border_thickness)
        for area in self.areas:
            area.display(screen, (0, 0, 0), offset)

    def display_update(self):
        screen = self.screen
        border_thickness = round(self.cellSize/10)
        offset = (border_thickness, border_thickness)
        while len(self.to_update):
            area = self.to_update.pop()
            area.display_update(screen, (0, 0, 0), offset)
    
    def display_solution(self):
        screen = self.screen
        border_thickness = round(self.cellSize/10)
        offset = (border_thickness, border_thickness)
        color_solution = (120, 120, 120) if not self.is_solved else (0, 175, 0)
        for cell in self.solution:
            cell.display(screen, color_solution, offset=offset)

    def display_start_end(self):
        screen = self.screen
        self.start.display(screen, (0, 255, 0), offset=self.offset)
        self.end.display(screen, (255, 0, 0), offset=self.offset)

    def break_wall(self):
        if len(self.areas) > 1:
            area = choice(self.areas)
            cell = choice(area.cells)
            x, y = cell.x, cell.y
            possible = self.check_adj(x, y)
            if len(possible):
                other_cell = choice(possible)
                other_area = self.get_area_of_cell(other_cell)
                if other_area is not None and other_area != area:
                    if other_cell.x > x:
                        cell.est = False
                    elif other_cell.x < x:
                        other_cell.est = False
                    elif other_cell.y > y:
                        cell.sud = False
                    else:
                        other_cell.sud = False
                    area.to_update.append(cell)
                    other_area.to_update.append(other_cell)
                    if other_area.power > area.power:
                        other_area.absorb(area)
                        self.areas.remove(area)
                        self.to_update.append(other_area)
                    else:
                        area.absorb(other_area)
                        self.areas.remove(other_area)
                        self.to_update.append(area)
        
    def solve(self):
        if not self.is_solved:
            last = self.solution.pop(-1)
            accessible = self.get_joinable(last.x, last.y)
            choosable = [cell for cell in accessible if not cell.is_in(self.visited)]
            
            if len(choosable):
                self.visited.append(choosable[0])
                self.solution.extend([last, choosable[0]])

                color_solution = (120, 120, 120) if not self.is_solved else (0, 175, 0)
                choosable[0].display(self.screen, color_solution, offset=self.offset)
            else:
                visited_color = (200, 200, 200) if not self.is_solved else (255, 255, 255)
                last.display(self.screen, visited_color, offset=self.offset)
            if self.solution[-1] == self.end:
                self.is_solved = True
    
    def solve_a_star(self):
        pass
    
    def update(self, breaking_speed, solving_speed):
        if not self.is_ready:
            self.display_update()
            if len(self.areas) == 1:
                self.is_ready = True
                self.display()
                self.display_start_end()
                self.pause = True
        if not self.pause:
            if not self.is_ready:
                if breaking_speed > 0:
                    breaking_speed = round(breaking_speed)
                    for _ in range(breaking_speed):
                        self.break_wall()
                else:
                    while not self.is_ready:
                        self.break_wall()
            elif not self.is_solved:
                if solving_speed > 0:
                    solving_speed = round(solving_speed)
                    for _ in range(solving_speed):
                        self.solve()
                else:
                    while not self.is_solved:
                        self.solve()
            else:
                self.display()
                self.display_solution()
                self.display_start_end()
    
    def save(self):
        screen = self.screen
        dimX, dimY = self.dim
        self.display()
        self.display_start_end()
        pygame.display.flip()
        path = env["USERPROFILE"] + "\\Pictures\\Mazes\\"
        filename = f"maze_{dimX}-{dimY}_{self.seed}"
        ext = ".png"
        if not self.is_ready:
            filename = "unfinished_" + filename
        pygame.image.save(screen, path + filename + ext)
        if self.is_solved:
            filename += "_solved"
            self.display_solution()
            self.display_start_end()
            pygame.image.save(screen, path + filename + ext)