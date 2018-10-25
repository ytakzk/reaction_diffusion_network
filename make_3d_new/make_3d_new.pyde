add_library('peasycam')

from rdn import *
from primitives import *
import octree as oc
from combinations import *
from io import *
from brick import *
import marching_cubes_3d as mc

cells = []
all_boxes = []
dist_list = []
name = '1790.csv'
LENGTH = 50
HEIGHT = 20
R = 5
sh = None

def setup():

    global cells, boxes, brick, sh, dist_list
    size(400, 400, P3D)

    cam = PeasyCam(this, LENGTH * 2)

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

        dist_list_y = []

        for x in range(LENGTH):
            cell = cells[y][x]
            v = (cell - min_val) / (max_val - min_val) * HEIGHT
            
            if v > HEIGHT * 0.5:
                v -= HEIGHT * 0.5
                cell = v
            else:
                v = HEIGHT * 0.5 - v
                cell = v
            
    for zz in range(HEIGHT):
        dist_list_yx = []
        z = zz - int(HEIGHT * 0.5)
        
        for y in range(LENGTH):
    
            dist_list_y = []

            for x in range(LENGTH):
                v = cells[y][x]
                
                if v >= 0:
                    k = sqrt(R ** 2 - v ** 2) 
                    d = sqrt(k ** 2 + z ** 2) - R
                else:
                    k = sqrt(R ** 2 - v ** 2) 
                    d = sqrt((2 * R - k) ** 2 + z ** 2) - R
                
                dist_list_y.append(d)
            dist_list_yx.append(dist_list_y)
        dist_list.append(dist_list_yx)

    # sh = createShape()
    # sh.beginShape(POINTS)

    # for z in range(HEIGHT):
    #     for y in range(LENGTH):
    #         for x in range(LENGTH):
    #             d = dist_list[z][y][x]
    #             stroke(random(0, 255), 0, 0)
    #             sh.setFill(color(random(0, 255), 0, 0))
    #             sh.setStroke(color(random(0, 255), 0, 0))
    #             sh.vertex(x * 3, y * 3, z * 3)
    # sh.endShape()
        
def draw():

    background(77)
    
    for z in range(HEIGHT):
        for y in range(LENGTH):
            for x in range(LENGTH):
                d = dist_list[z][y][x]
                
                if d > 0:
                    continue
                fill(d * 200, 0, 0)
                noStroke()
                pushMatrix()
                translate(x * 6, y * 6, z * 6)
                box(2)
                popMatrix()
    
    # shape(sh)
