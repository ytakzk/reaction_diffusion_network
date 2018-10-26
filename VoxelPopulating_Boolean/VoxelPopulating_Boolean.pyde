# this file is an illustration on how to fill a hole space with voxel values based on a 2D image
# prdouced based on a reaction diffusion algorithm
add_library('peasycam')

import map_loader
import writer

tile_name_a = 24
tile_name_b = 0

def setup():
    global box_list, imageWidth, imageHeight, z_range, half_zRange, side_length, maxValue, half_maxValue, boxSpacing, sides
    side_length = 200
    boxSpacing = 10

    sides = side_length * boxSpacing

    size(1000, 1000, P3D)
    cam = PeasyCam(this, sides / 2, sides / 2, 0, 500)
    unit_length = 10

    maxValue = 512
    half_maxValue = (maxValue) / 2
    # frameRate(4)

    cells_a = map_loader.load_map('2717/' + str(tile_name_a) + '.csv', maxValue, side_length)
    cells_b = map_loader.load_map('2717/' + str(tile_name_b) + '.csv', maxValue, side_length)

    # image1 = loadImage("200E2-2.png")
    # image2 = image1
    # image1 = loadImage("200E2-1.png")

    z_range = 16
    half_zRange = int(z_range / 2)

    global structure_radius, structural_radiusE2, radiusDivHalfMaxValue
    structural_radius = 3.6#3.2
    structural_radiusE2 = structural_radius

    radiusDivHalfMaxValue = structural_radius / half_maxValue
    print radiusDivHalfMaxValue

    # x direction
    global setA, setB
    setA, setB = [], []

    # sourceImage1
    
    extraValues = []
    
    
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = - cells_a[j][i]
            # colour = image1.get(i, j)
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
                extraValues.append(str(i) + ',' + str(j) + ',' + str(k) + ', raw_val: ' + str(colour) + ", x^2: " + str(xE2) + ', z: ' + str(z) + ', k: ' + str(k) )
            boxValue_list2D.append(boxValue_list1D)
        setA.append(boxValue_list2D)

    writer.writeBis(extraValues)
    
    # sourceImage2
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = cells_b[i][j]
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
            boxValue_list2D.append(boxValue_list1D)
        setB.append(boxValue_list2D)

    global booleanSet, zShift
    zShift = 4
    booleanSet = []
    booleanSet = booleanUnion(setA, setB, [side_length, side_length, z_range], zShift)
    
    writer.write(booleanSet, tile_name_a, tile_name_b)

def draw():
    background(127)

    strokeWeight(10)

    # for i in range(side_length):
    #     x = i * boxSpacing
    #     for j in range(side_length):
    #         y = j * boxSpacing

    #         for k in range(z_range):
    #             value = setA[i][j][k]
    #             if value < 0:
    #                 stroke(color(255, 0, 0))
    #                 z = k * boxSpacing
    #                 point(x, y, z)

    # for i in range(side_length):
    #     x = i * boxSpacing
    #     for j in range(side_length):
    #         y = j * boxSpacing

    #         for k in range(z_range):
    #             value = setB[i][j][k]
    #             if value < 0:
    #                 stroke(color(255, 0, 0))
    #                 z = k * boxSpacing
    #                 point(x, y, z + 100.0)

    for i in range(side_length):
        x = i * boxSpacing
        for j in range(side_length):
            y = j * boxSpacing

            for k in range(z_range + zShift):
                value = booleanSet[i][j][k]                
                if value < 0:
                    stroke(color(255, 0, 0))
                    z = k * boxSpacing
                    point(x, y, z + 100.0)

                # stroke(int(value*2.5))
                # z = k * boxSpacing
                # point(x, y, z)

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

def booleanUnion(setA, setB, setDimensions, zShiftB=0):
    newSet = []
    zShiftB = int(zShiftB)
    # get the voxelspace limits
    voxS_l = setDimensions[0]
    voxS_w = setDimensions[1]
    voxS_z = setDimensions[2]

    # get the dimensions of the  new voxel box
    voxN_l = voxS_l
    voxN_w = voxS_w
    voxN_z = voxS_z + abs(zShiftB)

    # creating the new set
    for x in range(voxN_l):
        listY = []
        for y in range(voxN_w):
            listZ = []
            for z in range(voxN_z):
                listZ.append(0)
            listY.append(listZ)
        newSet.append(listY)

    # dividing the two boolean surfaces into multiple zones
    if zShiftB < 0:
        # if surfaceB is shifted underneath surfaceA
        divisioning = 1
        voxN_z0 = 0
        voxN_z1 = - zShiftB
        voxN_z2 = voxS_z
        voxN_z3 = voxS_z - zShiftB
    elif zShiftB > 0:
        # if surfaceB is shifted above surfaceA
        divisioning = 2
        voxN_z0 = 0
        voxN_z1 = zShiftB
        voxN_z2 = voxS_z
        voxN_z3 = voxS_z + zShiftB
    elif zShiftB == 0:
        # if the two surfaces aren't shfited
        divisioning = 0
        voxN_z0 = 0
        voxN_z3 = voxS_z

    if divisioning == 0:

        test_length = 0
        for z in range(voxN_z0, voxN_z3, 1):
            test_length += 1

        print "real length: ", voxN_z
        print "test length: ", test_length
                
        for x in range(voxN_l):
            for y in range(voxN_w):
                for z in range(voxN_z0, voxN_z3, 1):
                    valueA = setA[x][y][z]
                    valueB = setB[x][y][z]
                    value = min(valueA, valueB)
                    newSet[x][y][z] = value

    elif divisioning == 1:
        test_length = 0
        for z in range(voxN_z0, voxN_z1, 1):
            test_length += 1
        for z in range(voxN_z1, voxN_z2, 1):
            test_length += 1
        for z in range(voxN_z2, voxN_z3, 1):
            test_length += 1

        print "real length: ", voxN_z
        print "test length: ", test_length
        
        for x in range(voxN_l):
            for y in range(voxN_w):
                for z in range(voxN_z0, voxN_z1, 1):
                    value = setB[x][y][z]
                    newSet[x][y][z] = value
                for z in range(voxN_z1, voxN_z2, 1):
                    valueA = setA[x][y][z + zShiftB]
                    valueB = setB[x][y][z]
                    value = min(valueA, valueB)
                    newSet[x][y][z] = value
                for z in range(voxN_z2, voxN_z3, 1):
                    value = setA[x][y][z + zShiftB]
                    newSet[x][y][z] = value

    elif divisioning == 2:
        test_length = 0
        for z in range(voxN_z0, voxN_z1, 1):
            test_length += 1
        for z in range(voxN_z1, voxN_z2, 1):
            test_length += 1
        for z in range(voxN_z2, voxN_z3, 1):
            test_length += 1

        print "real length: ", voxN_z
        print "test length: ", test_length
        
        for x in range(voxN_l):
            for y in range(voxN_w):
                for z in range(voxN_z0, voxN_z1, 1):
                    value = setA[x][y][z]
                    newSet[x][y][z] = value
                for z in range(voxN_z1, voxN_z2, 1):
                    valueA = setB[x][y][z - zShiftB]
                    valueB = setA[x][y][z]
                    value = min(valueA, valueB)
                    newSet[x][y][z] = value
                for z in range(voxN_z2, voxN_z3, 1):
                    value = setB[x][y][z - zShiftB]
                    newSet[x][y][z] = value

    return newSet
