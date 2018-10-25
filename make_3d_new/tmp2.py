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
        for x in range(LENGTH):
            cell = cells[y][x]
            v = (cell - min_val) / (max_val - min_val) * HEIGHT
            
            b = RDNBox(x, y, 0, 1, 1, v)

            # if v > HEIGHT * 0.5:
            #     v -= HEIGHT * 0.5
            #     b = RDNBox(x, y, v * 0.5, 1, 1, 5)
            #     positive_boxes.append(b)
            # else:
            #     v = HEIGHT * 0.5 - v
            #     b = RDNBox(x, y, -v * 0.5, 1, 1, 5)
            #     negative_boxes.append(b)
            all_boxes.append(b)

    brick = Brick(0, 0, 0, all_boxes, LENGTH, LENGTH)
    recalc_geom()

def recalc_geom():

    global sh
    
    mcmesh = Mesh()
    ot = oc.OcTree(Vector(0,0,0), 800.0)
    ot.set_level(5)
    ot.distobj = brick
    ot.divide(ot.rootnode, mcmesh)
    sh = get_pshape(mcmesh)


def draw():

    background(77)
    strokeWeight(0.5)
    
    directionalLight(255, 0, 127, 0, 0, -1)
    directionalLight(0, 127, 255, -1, 0, 0.3)
    directionalLight(127, 255, 0, 0.5, 1, 0.3)
    directionalLight(0, 255, 127, 0.5, -1, 0.3)
    shape(sh)
