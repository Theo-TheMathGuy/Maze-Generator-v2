import pygame
from maze import Maze

pygame.init()

## Maze Parameters ##
cellSize = 12
dim = (80, 80)
breaking_speed = 1
solving_speed = 1
limit_fps = False
FPS = 3

## Actual Code ##
MAX_HEIGHT = 990
MAX_WIDTH = 1920
width = cellSize * dim[0]
height = cellSize * dim[1]

dimX, dimY = dim
if width > MAX_WIDTH: dimX = dim[0]*MAX_WIDTH//width
if height > MAX_HEIGHT: dimY = dim[1]*MAX_HEIGHT//height
dim = (dimX, dimY)
WIDTH = cellSize * dim[0]
HEIGHT = cellSize * dim[1]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator V2")

running = True
clock = pygame.time.Clock()
maze = Maze(dim, cellSize, screen)

while running:
    maze.update(breaking_speed, solving_speed)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                maze = Maze(dim, cellSize, screen)
            if event.key == pygame.K_SPACE:
                maze.pause = not maze.pause
            if event.key == pygame.K_RETURN and maze.is_ready:
                maze.pause = False
                maze.is_solving = True
            if event.key == pygame.K_s:
                maze.save()
        if event.type == pygame.QUIT:
            running = False
    if limit_fps:
        clock.tick(FPS)