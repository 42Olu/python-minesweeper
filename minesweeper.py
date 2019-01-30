import pygame
import numpy as np
from random import randint
import math


white = (255,255,255)
black = (0,0,0)
red = (210, 83, 83)
grey = (200, 200, 200)
brown = (102, 51, 0)

grid_size = 15
cell_size = 35
line_thickness = 2
turd_anzahl = math.floor(grid_size*grid_size / 4)

display_w = grid_size*cell_size + line_thickness*grid_size - 1
display_h = grid_size*cell_size + line_thickness*grid_size - 1

pygame.init()
canvas = pygame.display.set_mode((display_w, display_h))
pygame.display.set_caption('Turdsweeper')
clock = pygame.time.Clock()
text = pygame.font.SysFont('monospace', 14)
turdImg = pygame.image.load('turd.png').convert_alpha()

class Cell:
    revealed = False
    neighbor_turds = 0
    marked = False

    def __init__(self, turd, x, y, i, j, farbe):
        self.turd = turd
        self.x = x
        self.y = y
        self.row = i
        self.col = j
        self.color = farbe
        self.n_turds = text.render(str(self.neighbor_turds), 0, black)

    def mark(self):
        self.marked = True
        
    def unmark(self):
        self.marked = False
    
    def reveal(self):
        self.revealed = True
        if self.turd:
            self.color = red
        else:
            self.color = grey
        if self.neighbor_turds == 0 and not self.turd:
            for i in range(-1, 2):
                for j in range(-1,2):
                    if(self.row + i >= 0 and self.row + i < grid_size and self.col + j >= 0 and self.col + j < grid_size):
                        if not cells[self.row + i][self.col + j].turd and not cells[self.row + i][self.col + j].revealed:
                            cells[self.row + i][self.col + j].reveal()    

    def draw(self):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, cell_size, cell_size), 0)
        if self.revealed and not self.turd and self.neighbor_turds > 0:
            canvas.blit(self.n_turds, (self.x + math.floor(cell_size/2)-3, self.y + math.floor(cell_size/2)-5))
        if self.marked:
            pygame.draw.polygon(canvas, brown, ((self.x, self.y), (self.x+ 10, self.y), (self.x, self.y + 10)), 0)
        if self.turd and self.revealed:
            canvas.blit(turdImg, (self.x+ 3, self.y+ 5))

    def count_neighbors(self):
        for i in range(-1, 2):
            for j in range(-1,2):
                if(self.row + i >= 0 and self.row + i < grid_size and self.col + j >= 0 and self.col + j < grid_size):
                    if(cells[self.row + i][self.col + j].turd):
                        self.neighbor_turds += 1
        self.n_turds = text.render(str(self.neighbor_turds), 0, ((255 - math.floor(255*float(self.neighbor_turds)/8))/2, (255 - math.floor(255*float(self.neighbor_turds)/8))/3, 255 - math.floor(255*float(self.neighbor_turds)/8)))


def draw_cells():
    for i in range(0,grid_size):
        for j in range(0, grid_size):
            cells[i][j].draw()

def resolve_cell(r, c):
    i = 0
    j = 0
    while cells[i+1][0].y < r:
        i += 1
        if i == grid_size-1:
            break
    while j < grid_size and cells[0][j+1].x < c:
        j += 1
        if j == grid_size-1:
            break
    return j,i

def you_lose():
    for i in range(0,grid_size):
        for j in range(0, grid_size):
            cells[i][j].reveal()

def turd_placing():
    global cells

    for i in range(0,turd_anzahl):
        x = randint(0, grid_size-1)
        y = randint(0, grid_size-1)
        if cells[x][y].turd:
            i -= 1
        cells[x][y].turd = True
           
def count_neighbor_turds():
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            if not cells[i][j].turd:
                cells[i][j].count_neighbors()


beendet = False
verloren = False

#Make Cells Array
cell_type = np.dtype(Cell)
cells = np.empty([grid_size, grid_size], dtype=cell_type)

for i in range(0,grid_size):
    for j in range(0, grid_size):
        cells[i][j] = Cell(False, j*cell_size + j*line_thickness, i*cell_size +i*line_thickness, i, j, white)

turd_placing()
draw_cells()
count_neighbor_turds()

while not beendet:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            beendet = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                beendet = True
                
        if not verloren:        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0]:
                    pos = pygame.mouse.get_pos()
                    i, j = resolve_cell(pos[0], pos[1])
                    if cells[i][j].turd:
                        you_lose()
                        verloren = True
                    else:
                        cells[i][j].reveal()
                        
                if mouse_buttons[2]:
                    pos = pygame.mouse.get_pos()
                    i, j = resolve_cell(pos[0], pos[1])
                    if cells[i][j].marked:
                        cells[i][j].unmark()
                    else:
                        cells[i][j].mark()
                    
                draw_cells()    
    
    pygame.display.update()
    clock.tick(60)

   
pygame.quit()
