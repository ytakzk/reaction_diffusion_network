# this file is an illustration on how to fill a hole space with voxel values based on a 2D image
# prdouced based on a reaction diffusion algorithm
add_library('peasycam')

import map_loader
import writer
import voxel_operation
import boolean_operation

tile_name_a = 0
tile_name_b = 1

side_length = 80
boxSpacing = 10

max_value = 256
z_range   = 16
PATH = '../reactive_diffusion_network_java/output/'

def setup():

    sides = side_length * boxSpacing

    size(1000, 1000, P3D)
    cam = PeasyCam(this, sides / 2, sides / 2, 0, 1400)
    unit_length = 10
    
    cells_a = map_loader.load_map(PATH + '1823/' + str(tile_name_a) + '.csv', max_value, side_length)
    cells_b = map_loader.load_map(PATH + '1823/' + str(tile_name_b) + '.csv', max_value, side_length)

    # x direction
    global setA, setB
    
    setA, _ = voxel_operation.create_3d_array(cells=cells_a, side_length=side_length, z_range=z_range, max_value=max_value, is_positive=False)
    setB, _ = voxel_operation.create_3d_array(cells=cells_b, side_length=side_length, z_range=z_range, max_value=max_value)


    global booleanSet
    booleanSet = boolean_operation.union(setA, setB, 6)
    
    writer.write(booleanSet, tile_name_a, tile_name_b)

def draw():
    background(127)

    strokeWeight(10)

    for i in range(side_length):
        x = i * boxSpacing
        for j in range(side_length):
            y = j * boxSpacing

            for k in range(z_range):
                value = setA[i][j][k]
                if value < 0:
                    stroke(color(0, 0, 255))
                    z = k * boxSpacing
                    point(x, y, z)

    for i in range(side_length):
        x = i * boxSpacing
        for j in range(side_length):
            y = j * boxSpacing

            for k in range(z_range):
                value = setB[i][j][k]
                if value < 0:
                    stroke(color(0, 255, 0))
                    z = k * boxSpacing
                    point(x, y, z + 300.0)

    z_len = len(booleanSet[0][0])
    for i in range(side_length):
        x = i * boxSpacing
        for j in range(side_length):
            y = j * boxSpacing

            for k in range(z_len):
                value = booleanSet[i][j][k]                
                if value < 0:
                    stroke(color(0, 255 * float(k) / z_len, 255 * (1.0 - float(k) / z_len)))
                    z = k * boxSpacing
                    point(x, y, z + 150)
