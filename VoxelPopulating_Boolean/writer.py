import writer

def write(data, tile_a_name, tile_b_name):
    
    x_len = len(data)
    y_len = len(data[0])
    z_len = len(data[0][0])
    
    output = createWriter('./output/%s_%s.csv' % (tile_a_name, tile_b_name))
    
    output.println('%d,%d,%d' % (x_len, y_len, z_len))
    
    for x in range(x_len):
        for y in range(y_len):
            for z in range(z_len):
                output.println('%d,%d,%d,%.3f' % (x, y, z, data[x][y][z]))
    
    output.flush()
    output.close()

def writeBis(data):
    
    output = createWriter('outputBugtesting.csv')
    
    for d in(data):
        output.println(d)
    
    output.flush()
    output.close()

    
    
