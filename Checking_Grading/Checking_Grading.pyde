import csv
import math as m

# this sketch maps out a set of values onto a csv

def setup():
    size(500,500)
    zValues = []
    imageQMark = False
    if imageQMark:
        imageSize = 468
        sourceImage = loadImage("SourceTestImage.png")
        for i in range(imageSize):
            for j in range(imageSize):
                colVs = sourceImage.get(i,j)
                colV = float(red(colVs))
                zValues.append(colV)
            
    elif not(imageQMark):
        name = "941.csv"
        file = open(name, 'r')
        lines = file.readlines()
        with open(name) as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                zValues.append(float(row[2]))
    
    res_bracks = []
    max_value = max(zValues)
    min_value = min(zValues)
    delta = max_value - min_value
    
    global resolutionCount, resolution
    resolution = 20
    resolutionCount = []
    deltaOverResolution = delta / resolution
    
    for i in range(len(zValues)):
        zValues[i] -= min_value
        zValues[i] = 2 * zValues[i] / delta
        zValues[i] -= 1.0
        # zValues[i] = 
        
        power = 1.0
        if zValues[i] != 0:
            zValues[i] = m.pow((2.0 * abs(zValues[i]) - zValues[i]**2), power)*zValues[i]/abs(zValues[i])
        else:
            zValues[i] = 0
        
        # number = .001
        # # powering
        # if zValues[i] == 1:
        #     power = 1
        # else:
        #     power = 1 + abs(number/(1-zValues[i]))
        
        # if zValues[i] != 0:
        #     zValues[i] = m.pow((2.0 * abs(zValues[i]) - zValues[i]**2), power)*zValues[i]/abs(zValues[i])
        # else:
        #     zValues[i] = 0
    
    for i in range(resolution):
        resolutionCount.append(0)
        
    max_value = + 1.0
    min_value = - 1.0
    delta = max_value - min_value
    deltaOverResolution = delta / resolution
    
    for i in range(resolution+1):
        bracket = i * deltaOverResolution - 1.0
        res_bracks.append(bracket)
    
    for zValue in zValues:
        for i in range(0, resolution, 1):
            if (zValue >= res_bracks[i] and zValue < res_bracks[i+1]):
                resolutionCount[i] += 1
    
    # plotting out reference functions
    global resolutionCount_y, res_bracks_y, yValues
    items = 2000
    halfItems = items/2.0
    resolutionCount_y = []
    res_bracks_y = []
    yValues = []
    max_value = + 1.0
    min_value = - 1.0
    delta = max_value - min_value
    deltaOverResolution = delta / resolution
    print deltaOverResolution
     
    for i in range(resolution):
        resolutionCount_y.append(0)
    
    for i in range(resolution+1):
        bracket = i * deltaOverResolution - 1.0
        res_bracks_y.append(bracket)
        
    for j in range(- int(halfItems), int(halfItems), 1):
        for i in range(0, resolution, 1):
            itemValue = j / halfItems
            zValue = function(itemValue)

            if (zValue >= res_bracks_y[i] and zValue < res_bracks_y[i+1]):
                resolutionCount_y[i] += 1
    
def function(input):
    if input != 0:
        output = sqrt(2.0 * abs(input) - input**2)*input/abs(input)
    else:
        output = 0
    return output

def draw():
    max_value = max(resolutionCount)
    max_value_y = max(resolutionCount_y)
    recHeightDelta = float(height)/max_value
    recHeightDelta_y = float(height)/max_value_y
    recWidth = float(width)/resolution             
    for i in range(resolution):
        noStroke()
        strokeWeight(0)
        fill(255)
        recHeight = recHeightDelta * resolutionCount[i]
        rect(i*recWidth, height - recHeight, recWidth, recHeight)
        noFill()
        strokeWeight(1)
        stroke(color(255,0,0))
        recHeight = recHeightDelta_y * resolutionCount_y[i]
        rect(i*recWidth, height - recHeight, recWidth, recHeight)
