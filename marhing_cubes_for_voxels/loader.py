import math

def load(tile_name_a, tile_name_b):
    
    name = '../VoxelPopulating_Boolean/output/%s_%s.csv' % (tile_name_a, tile_name_b)
        
    file = open(name, 'r')
    lines = file.readlines()
    
    x_len, y_len, z_len = lines[0].replace('\n', '').split(',')
    
    x_len = int(x_len) + 2
    y_len = int(y_len) + 2
    z_len = int(z_len) + 2
    
    data = []
    for x in range(x_len):
        data_yz = []
        for y in range(y_len):
            data_z = []
            for z in range(z_len):
                data_z.append(1)
            data_yz.append(data_z)
        data.append(data_yz)
        
    for l in lines[1:]:

        x, y, z, v = l.replace('\n', '').split(',')

        x = int(x)
        y = int(y)
        z = int(z)
        v = float(v)
        
        if math.isnan(v):
            v = 1.0
            
        data[x+1][y+1][z+1] = v
        
    # for y in range(y_len):
    #     for z in range(z_len):
    #         data[x_len-1][y][z] = data[1][y][z] 
    #         data[0][y][z] = data[x_len-2][y][z] 

    # for x in range(x_len):
    #     for z in range(z_len):
    #         data[x][y_len-1][z] = data[x][1][z] 
    #         data[x][0][z] = data[x][y_len-2][z] 
        
    return data, x_len, y_len, z_len
