def getValidPosition(width, height, playerPos, minimumRadiusDistance):
    x = random.randint(0, width-1)
    minY = 0

    if abs(x - playerPos[0]) < minimumRadiusDistance:
        minY = playerPos[1] + minimumRadiusDistance
   
    y = random.randint(minY, height-1)

    return (x,y)


# remember that this assumes playerPos is a list or tuple containing x, y coordinates
# these are indexed in the code as playerPos[0] and playerPos[1]

