from cell import *

cells = []

LENGTH = 400

def setup():
    size(LENGTH, LENGTH)
    colorMode(HSB)
    
    for y in range(LENGTH):
        cells_y = []
        for x in range(LENGTH):
            
            if x > LENGTH * 0.5 - 5 and x < LENGTH * 0.5 + 5 and y > LENGTH * 0.5 - 5 and y < LENGTH * 0.5 + 5:
                u = 1
                v = 1
            else:
                u = 1
                v = 0
                
            cell = Cell(x, y, u, v)
            cells_y.append(cell)
        cells.append(cells_y)
        
    for y in range(LENGTH):
        for x in range(LENGTH):
            cell = cells[y][x]
            
            next_x = abs((x + 1) % LENGTH)
            prev_x = abs((x - 1) % LENGTH)
            next_y = abs((y + 1) % LENGTH)
            prev_y = abs((y - 1) % LENGTH)

            c1 = cells[next_y][x]
            c2 = cells[prev_y][x]
            c3 = cells[y][next_x]
            c4 = cells[y][prev_x]
            c5 = cells[next_y][next_x]
            c6 = cells[next_y][prev_x]
            c7 = cells[prev_y][next_x]
            c8 = cells[prev_y][prev_x]            
            cell.neighbors.extend([c1, c2, c3, c4, c5, c6, c7, c8])
            cell.r_neighbors.extend([0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05])       
    
def draw():
    
    for y in range(1, LENGTH-1):
        for x in range(1, LENGTH-1):
            cell = cells[y][x]
            cell.calculate()

    loadPixels()
    for y in range(LENGTH):
        for x in range(LENGTH):
            cell = cells[y][x]
            cell.update()
            h = (cell.u - cell.v) * 255
            pixels[x + y * LENGTH] = color(h, 255, 255)
    updatePixels()
    
def mousePressed():
    cell = cells[mouseY][mouseX]
    cell.v = 1
