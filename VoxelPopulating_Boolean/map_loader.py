def load_map(name, upper_bound, LENGTH):

    cells = []
    for y in range(LENGTH):
        cells_y = []
        for x in range(LENGTH):
            cells_y.append(0)
        cells.append(cells_y)
        
    file = open('../reactive_diffusion_network_java/output/' + name, 'r')
    lines = file.readlines()

    min_val = 999
    max_val = -999
    for l in lines:

        l = l.replace('\n', '')
        y, x, v = l.split(',')

        y = int(y)
        x = int(x)
        v = float(v)

        cells[y][x] = v

        if v > max_val:
            max_val = v
        elif v < min_val:
            min_val = v

    sum = 0.0
    num = 0
    for y in range(LENGTH):
        for x in range(LENGTH):
            cell = cells[y][x]
            v = (cell - min_val) / (max_val - min_val) * upper_bound
            v -= upper_bound / 2
            cells[y][x] = v
            sum += v
            num += 1
    
    print('the average is %f' % (sum / float(num)))
    

    return cells
