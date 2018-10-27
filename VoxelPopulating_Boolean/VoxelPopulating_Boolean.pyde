# this file is an illustration on how to fill a hole space with voxel values based on a 2D image
# prdouced based on a reaction diffusion algorithm
add_library('peasycam')

import map_loader
import writer
import boolean_operation

tile_name_a = 0
tile_name_b = 1

side_length = 80
boxSpacing = 10

def setup():
    global box_list, imageWidth, imageHeight, z_range, half_zRange, side_length, maxValue, half_maxValue, boxSpacing, sides

    sides = side_length * boxSpacing

    size(1000, 1000, P3D)
    cam = PeasyCam(this, sides / 2, sides / 2, 0, 1400)
    unit_length = 10

    maxValue = 256
    half_maxValue = (maxValue) / 2

    cells_a = map_loader.load_map('1823/' + str(tile_name_a) + '.csv', maxValue, side_length)
    cells_b = map_loader.load_map('1823/' + str(tile_name_b) + '.csv', maxValue, side_length)

    z_range = 16
    half_zRange = int(z_range / 2)

    global structural_radius, structural_radiusE2, radiusDivHalfMaxValue
    structural_radius = 3.6#3.2
    structural_radiusE2 = structural_radius

    radiusDivHalfMaxValue = structural_radius / half_maxValue
    print radiusDivHalfMaxValue

    # x direction
    global setA, setB
    setA, setB = [], []

    # sourceImage1
    
    setA = create_3d_array(cells_a, False)
    setB = create_3d_array(cells_b)

    global booleanSet
    booleanSet = boolean_operation.union(setA, setB, 6)
    
    writer.write(booleanSet, tile_name_a, tile_name_b)

def create_3d_array(cells, is_positive=True, generate_log=False):
    
    sign = 1 if is_positive else -1
    
    logs = []
    
    sets = []
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = sign * cells[i][j]
            # colour = image2.get(i, j)
            # colour = red(colour) - half_maxValue
            xE2 = fromZtoX2(colour)
            # z direction
            boxValue_list1D = []
            for k in range(z_range):
                z = k - half_zRange
                d = xE2 + z ** 2
                if d < 0:
                    d = 0
                value = sqrt(d) - structural_radius
                boxValue_list1D.append(value)
                logs.append(str(i) + ',' + str(j) + ',' + str(k) + ', raw_val: ' + str(colour) + ", x^2: " + str(xE2) + ', z: ' + str(z) + ', k: ' + str(k) )

            boxValue_list2D.append(boxValue_list1D)
        sets.append(boxValue_list2D)
        
    if generate_log:
        writer.writeBis(log)
        
    return sets

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

def fromZtoX2(zValue):
    # normalisation as if it the surface was constructed out of a set of
    # cylinders
    zValue *= radiusDivHalfMaxValue * .8
    # differentiating for values that are below and above the z-plane
    zValueE2 = zValue ** 2
    if zValue >= 0.0:
        x2 = structural_radiusE2 - zValueE2
    else:        
        if zValueE2 > structural_radiusE2:
            x2 = 100
        else: 
            x_negative2 = structural_radiusE2 - zValueE2
            x_negative = sqrt(x_negative2)
            x = 2 * structural_radiusE2 - x_negative
            x2 = x ** 2
    return x2
