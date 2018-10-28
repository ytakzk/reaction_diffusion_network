import math

def create_3d_array(cells, side_length, max_value, z_range, structural_radius=3.6, is_positive=True):
    
    half_zRange = int(z_range / 2)
    radius_divided_by_half_max_value = structural_radius / (max_value * 0.5)

    sign = 1 if is_positive else -1
    
    logs = []
    
    sets = []
    for i in range(side_length):
        # y direction
        boxValue_list2D = []
        for j in range(side_length):
            colour = sign * cells[i][j]
            xE2 = from_z_to_x2(colour, radius_divided_by_half_max_value, structural_radius)
            # z direction
            boxValue_list1D = []
            for k in range(z_range):
                z = k - half_zRange
                d = xE2 + z ** 2
                if d < 0:
                    d = 0
                value = math.sqrt(d) - structural_radius
                boxValue_list1D.append(value)
                logs.append(str(i) + ',' + str(j) + ',' + str(k) + ', raw_val: ' + str(colour) + ", x^2: " + str(xE2) + ', z: ' + str(z) + ', k: ' + str(k) )

            boxValue_list2D.append(boxValue_list1D)
        sets.append(boxValue_list2D)
        
    return sets, logs

def from_z_to_x2(zValue, radius_divided_by_half_max_value, structural_radius):
    # normalisation as if it the surface was constructed out of a set of
    # cylinders
    zValue *= radius_divided_by_half_max_value * .8
    # differentiating for values that are below and above the z-plane
    zValueE2 = zValue ** 2
    if zValue >= 0.0:
        x2 = structural_radius - zValueE2
    else:        
        if zValueE2 > structural_radius:
            x2 = 100
        else: 
            x_negative2 = structural_radius - zValueE2
            x_negative = math.sqrt(x_negative2)
            x = 2 * structural_radius - x_negative
            x2 = x ** 2
    return x2
