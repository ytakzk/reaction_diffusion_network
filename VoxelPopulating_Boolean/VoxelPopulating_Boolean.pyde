# this file is an illustration on how to fill a hole space with voxel values based on a 2D image
# prdouced based on a reaction diffusion algorithm
add_library('peasycam')

def setup():
    size(1000, 1000, P3D)
    cam = PeasyCam(this, 1000, 1000, 0, 500)
    global box_list, imageWidth, imageHeight, z_range, half_zRange, side_length
    side_length = 25
    unit_length = 10
    # frameRate(4)
    
    sourceImage1 = loadImage("25E2.png")
    sourceImage2 = loadImage("25E2B.png")
    z_range = 16
    half_zRange = int(z_range/2)
    
    global structure_radius, structural_radiusE2, maxValue, half_maxValue, radiusDivHalfMaxValue, boxSpacing
    structural_radius = 3.2
    structural_radiusE2 = structural_radius
    maxValue = 128.0
    half_maxValue = (maxValue)/2
    radiusDivHalfMaxValue = structural_radius / half_maxValue
    boxSpacing = 10
    
    # x direction
    global setA, setB
    setA, setB = [], []
    
    # sourceImage1
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = sourceImage1.get(i, j)
            colour = red(colour) - 128
            xE2 = fromZtoX2(colour)
            # z direction
            boxValue_list1D = []
            for k in range(z_range):
                z = k - half_zRange
                value = sqrt(xE2 + z**2) - structural_radius
                boxValue_list1D.append(value)
            boxValue_list2D.append(boxValue_list1D)
        setA.append(boxValue_list2D)
    
    # sourceImage2
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = sourceImage2.get(i, j)
            colour = red(colour) - 128
            xE2 = fromZtoX2(colour)
            # z direction
            boxValue_list1D = []
            for k in range(z_range):
                z = k - half_zRange
                value = sqrt(xE2 + z**2) - structural_radius
                boxValue_list1D.append(value)
            boxValue_list2D.append(boxValue_list1D)
        setB.append(boxValue_list2D)
        
    global booleanSet
    booleanSet = []
    booleanSet = booleanUnion(setA, setB, [side_length, side_length, z_range], 15)

def draw():
    background(127)
    
    strokeWeight(10)
                
    for i in range(side_length):
        x = i * boxSpacing
        for j in range(side_length):
            y = j * boxSpacing
            for k in range(z_range + 15):
                value = booleanSet[i][j][k]
                if value < 0:
                    stroke(color(255,0,0))
                    z = k * boxSpacing
                    point(x, y, z)
    
def fromZtoX2(zValue):
    # normalisation as if it the surface was constructed out of a set of cylinders
    zValue *= radiusDivHalfMaxValue
    # differentiating for values that are below and above the z-plane
    if zValue >= 0.0:
        x2 = structural_radiusE2 - zValue**2
    else:
        x_negative2 = structural_radiusE2 - zValue**2
        x_negative = sqrt(x_negative2)
        x = 2*structural_radiusE2 - x_negative
        x2 = x**2
    return x2

def booleanUnion(setA, setB, setDimensions, zShiftB = 0):
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
         for x in range(voxN_l):
            for y in range(voxN_w):
                for z in range(voxN_z0, voxN_z3, 1):
                    valueA = setA[x][y][z]
                    valueB = setB[x][y][z]
                    value = min(valueA, valueB)
                    newSet[x][y][z] = value
    
    elif divisioning == 1:
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
                for z in range(voxN_z0, voxN_z1, 1):
                    value = setA[x][y][z + zShiftB]
                    newSet[x][y][z] = value
                    
    elif divisioning == 2:
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
                for z in range(voxN_z0, voxN_z1, 1):
                    value = setB[x][y][z - zShiftB]
                    newSet[x][y][z] = value
                    
    return newSet
    
