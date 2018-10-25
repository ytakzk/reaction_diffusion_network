add_library('peasycam')

from rdn import *
from primitives import *
import octree as oc
from combinations import *
from io import *

cells = []
positive_boxes = []
negative_boxes = []
all_boxes      = []
name = '2595.csv'
LENGTH = 250
HEIGHT = 60

def setup():
    
    global cells, boxes
    size(LENGTH * 2, LENGTH * 2, P3D)
    
    cam = PeasyCam(this, 400)
    
    for y in range(LENGTH):
        cells_y = []
        for x in range(LENGTH):
            cells_y.append(0)
        cells.append(cells_y)
            
    
    file = open('../reactive_diffusion_network_java/output/' + name, 'r') 
    lines = file.readlines() 
    
    min_val = 999
    max_val = -999
    for l in lines:
            
            l = l.replace('\n', '')
            y, x, v = l.split(',')
            
            y = int(y)
            x = int(x)
            v = float(v)
            
            cells[y][x] = v
            
            if v > max_val:
                max_val = v
            elif v < min_val:
                min_val = v
                        
    for y in range(LENGTH):
        y_all_boxes = []
        for x in range(LENGTH):
            cell = cells[y][x]
            v = (cell - min_val) / (max_val - min_val) * HEIGHT
                        
            if v > HEIGHT * 0.5:
                v -= HEIGHT * 0.5
                b = RDNBox(x, y, v * 0.5, 1, 1, 5)
                positive_boxes.append(b)
            else:
                v = HEIGHT * 0.5 - v
                b = RDNBox(x, y, -v * 0.5, 1, 1, 5)
                negative_boxes.append(b)
            y_all_boxes.append(b)
        all_boxes.append(y_all_boxes)

    # for y in range(LENGTH):
    #     for x in range(LENGTH):
    #         b = all_boxes[y][x]
            
    #         neighbors = []
            
    #         diff = 3
            
    #         for xx in range(x-diff, x+diff):
    #             for yy in range(y-diff, y+diff):

    #                 nx = abs(xx % LENGTH)
    #                 ny = abs(yy % LENGTH)
    
    #                 n  = all_boxes[ny][nx]
    #                 neighbors.append(n)
                
    #         sum_z = 0.0
    #         sum_c = 0.0
    #         for n in neighbors:
    #             sum_z += n.loc.z
    #             sum_c += n.c
    #         sum_z /= len(neighbors)
    #         sum_c /= len(neighbors)
            
    #         b.c = sum_c
    #         b.loc.z = sum_z


def draw():

    background(77)
    strokeWeight(0.5)
    
    fill(255, 0, 0)
    for b in positive_boxes:
        b.draw()

    fill(0, 255, 0)
    for b in negative_boxes:
        b.draw()
