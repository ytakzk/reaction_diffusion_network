def union(lhs, rhs, rhs_offset_z=0):

    x_len = len(lhs)
    y_len = len(lhs[0])
    z_len = len(lhs[0][0])
    
    if x_len != len(rhs) or y_len != len(rhs[0]) or z_len != len(rhs[0][0]):
        raise ValueError('The dimension must be same')
        
    if rhs_offset_z < 0:
        raise ValueError('rhs_offset_z must be positive')
        
    union_z_len = z_len + rhs_offset_z 
    
    arr = []
    for x in range(x_len):
        list_yz = []
        for y in range(y_len):
            list_z = []
            for z in range(union_z_len):
                list_z.append(0)
            list_yz.append(list_z)
        arr.append(list_yz)
    
    for x in range(x_len):
        for y in range(y_len):
            for z in range(union_z_len):
                
                if z < rhs_offset_z:
                    arr[x][y][z] = lhs[x][y][z]
                elif z < z_len:
                    lhs_v = lhs[x][y][z]
                    rhs_v = rhs[x][y][z - rhs_offset_z]
                    arr[x][y][z] = min(lhs_v, rhs_v)
                else:
                    arr[x][y][z] = rhs[x][y][z - rhs_offset_z]
                
    return arr
