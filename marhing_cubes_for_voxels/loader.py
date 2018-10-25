def load():
    
    name = '../VoxelPopulating_Boolean/output.csv'
        
    file = open(name, 'r')
    lines = file.readlines()
    
    x_len, y_len, z_len = lines[0].replace('\n', '').split(',')
    
    x_len = int(x_len)
    y_len = int(y_len)
    z_len = int(z_len)
    
    data = []
    for x in range(x_len):
        data_yz = []
        for y in range(y_len):
            data_z = []
            for z in range(z_len):
                data_z.append(0)
            data_yz.append(data_z)
        data.append(data_yz)
        
    for l in lines[1:]:

        x, y, z, v = l.replace('\n', '').split(',')

        x = int(x)
        y = int(y)
        z = int(z)
        v = float(v)
        data[x][y][z] = v
        
    return data, x_len, y_len, z_len
