add_library('peasycam')

from marching_cubes_3d import *
from primitives import *
from io import *
import loader

voxels = []
LENGTH = 100
HALF_LENGTH = int(LENGTH * 0.5)

tile_name_a = 1
tile_name_b = 0

def setup():

    global sh, data, x_len, y_len, z_len

    cam = PeasyCam(this, 200)

    size(1000, 1000, P3D)

    data, x_len, y_len, z_len = loader.load(tile_name_a, tile_name_b)

    mesh = Mesh()

    d = 1
    for x in range(0, x_len - 1, d):
        for y in range(0, y_len, d):
            for z in range(0, z_len - 1, d):

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

                if x + d > x_len - 1:
                    xd = x_len - 1 - x
                else:
                    xd = d

                if y + d > y_len - 1:
                    yd = y_len - 1 - y
                else:
                    yd = d

                if z + d > z_len - 1:
                    zd = z_len - 1 - z
                else:
                    zd = d

                v1 = data[x][y][z]
                v2 = data[x + xd][y][z]
                v3 = data[x + xd][y + yd][z]
                v4 = data[x][y + yd][z]
                v5 = data[x][y][z + zd]
                v6 = data[x + xd][y][z + zd]
                v7 = data[x + xd][y + yd][z + zd]
                v8 = data[x][y + yd][z + zd]

                distances = [v1, v2, v3, v4, v5, v6, v7, v8]

                mc = marching_cubes_3d_single_cell(distances, x, y, z, d)

                mesh.add_faces(mc.faces)
                for n in mc.nodes:
                    mesh.add_node(n)

    # mesh = generate_sphere()

    stroke(255)
    strokeWeight(0.5)
    sh = get_pshape(mesh)

    export_obj(mesh, filename='./output/%s_%s.obj' %
               (tile_name_a, tile_name_b))

def draw():

    background(0)

    directionalLight(255, 0, 127, 0, 0, -1)
    directionalLight(0, 127, 255, -1, 0, 0.3)
    directionalLight(127, 255, 0, 0.5, 1, 0.3)
    directionalLight(0, 255, 127, 0.5, -1, 0.3)

    # for x in range(0, x_len-1):
    #     for y in range(0, y_len-1):
    #         for z in range(0, z_len-1):
    #             if data[x][y][z] < 0:
    #                 point(x, y, z)

    shape(sh)


def generate_sphere():

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
    for x in range(0, LENGTH - 1, d):
        for y in range(0, LENGTH - 1, d):
            for z in range(0, LENGTH - 1, d):

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

                v1 = cells[x][y][z]
                v2 = cells[x + xd][y][z]
                v3 = cells[x + xd][y + yd][z]
                v4 = cells[x][y + yd][z]
                v5 = cells[x][y][z + zd]
                v6 = cells[x + xd][y][z + zd]
                v7 = cells[x + xd][y + yd][z + zd]
                v8 = cells[x][y + yd][z + zd]

                distances = [v1, v2, v3, v4, v5, v6, v7, v8]

                ratio = 5
                mc = marching_cubes_3d_single_cell(
                    distances, x * ratio, y * ratio, z * ratio, d)

                mesh.add_faces(mc.faces)
                for n in mc.nodes:
                    mesh.add_node(n)

    return mesh
