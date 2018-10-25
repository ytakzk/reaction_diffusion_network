add_library('peasycam')

from marching_cubes_3d import *
from primitives import *
from io import *

voxels = []
LENGTH = 100
HALF_LENGTH = int(LENGTH * 0.5)

def setup():
    
    global sh
    
    cam = PeasyCam(this, 200)
    
    size(300, 300, P3D)
    
    sp = Sphere(cx=HALF_LENGTH, cy=HALF_LENGTH, cz=HALF_LENGTH, rad=49)
    
    cells = []
    for x in range(LENGTH):
        cells_yz = []
        for y in range(LENGTH):
            cells_z = []
            for z in range(LENGTH):
                d = sp.get_distance(x, y, z)
                cells_z.append(d)
            cells_yz.append(cells_z)
        cells.append(cells_yz)
        
    mesh = Mesh()
        
    d = 5
    for x in range(0, LENGTH-1, d):
        for y in range(0, LENGTH-1, d):
            for z in range(0, LENGTH-1, d):
                
                # The order must be the followings.
                # VERTICES = [
                #     (0, 0, 0),
                #     (1, 0, 0),
                #     (1, 1, 0),
                #     (0, 1, 0),
                #     (0, 0, 1),
                #     (1, 0, 1),
                #     (1, 1, 1),
                #     (0, 1, 1),
                # ]
                
                if x + d > LENGTH - 1:
                    xd = LENGTH - 1 - x
                else:
                    xd = d
                    
                if y + d > LENGTH - 1:
                    yd = LENGTH - 1 - y
                else:
                    yd = d
                    
                if z + d > LENGTH - 1:
                    zd = LENGTH - 1 - z
                else:
                    zd = d
                                        
                v1 = cells[x   ][y   ][z   ]
                v2 = cells[x+xd][y   ][z   ]
                v3 = cells[x+xd][y+yd][z   ]
                v4 = cells[x   ][y+yd][z   ]
                v5 = cells[x   ][y   ][z+zd]
                v6 = cells[x+xd][y   ][z+zd]
                v7 = cells[x+xd][y+yd][z+zd]
                v8 = cells[x   ][y+yd][z+zd]

                distances = [v1, v2, v3, v4, v5, v6, v7, v8]

                mc = marching_cubes_3d_single_cell(distances, x, y, z, d)

                mesh.add_faces(mc.faces)
                for n in mc.nodes:
                    mesh.add_node(n)

    print(len(mesh.faces))
    stroke(255)
    strokeWeight(2)
    
    sh = get_pshape(mesh)
    
def draw():
    
    background(0)
    
    directionalLight(255,  0,127,  0,  0,  -1)
    directionalLight(  0,127,255,  -1, 0, 0.3)
    directionalLight(127,255,  0, 0.5, 1, 0.3)
    directionalLight(  0,255,127, 0.5,-1, 0.3)
    
    shape(sh)