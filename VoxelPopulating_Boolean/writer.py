def write(data):
    
    x_len = len(data)
    y_len = len(data[0])
    z_len = len(data[0][0])
    
    output = createWriter('output.csv')
    
    output.println('%d,%d,%d' % (x_len, y_len, z_len))
    
    for z in range(z_len):
        for y in range(y_len):
            for x in range(x_len):
                output.println('%d,%d,%d,%.3f' % (x, y, z, data[x][y][z]))
    
    output.flush()
    output.close()

    
