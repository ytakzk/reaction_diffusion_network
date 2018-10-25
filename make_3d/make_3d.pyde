add_library('peasycam')

from rdn import *
from primitives import *
import octree as oc
from combinations import *
from io import *
from brick import *
import marching_cubes_3d as mc

cells = []
positive_boxes = []
negative_boxes = []
all_boxes = []
name = '4196.csv'
LENGTH = 200
HEIGHT = 60
sh = None

def setup():

    global cells, boxes, brick
    size(LENGTH * 3, LENGTH * 3, P3D)

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
        for x in range(LENGTH):
            cell = cells[y][x]
            v = (cell - min_val) / (max_val - min_val) * HEIGHT
            
            if v > HEIGHT * 0.5:
                v -= HEIGHT * 0.5
                
                for z in range(int(v)):
                    b = RDNBox(x, y, z, 1, 1, 1)
                    positive_boxes.append(b)
            else:
                v = HEIGHT * 0.5 - v

                for z in range(int(v)):
                    b = RDNBox(x, y, -z, 1, 1, 1)
                    positive_boxes.append(b)
                                
                negative_boxes.append(b)
            all_boxes.append(b)


def draw():

    background(77)
    # strokeWeight(0.5)
    noStroke()
    
    # translate(width * 0.5, height * 0.5)
    
    for b in positive_boxes:
        fill( b.loc.z / 30.0 * 255, 0, 0)
        b.draw()

    for b in negative_boxes:
        fill(0, -b.loc.z / 30.0 * 255, 0)
        b.draw()
