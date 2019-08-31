import random

def getValidPosition(width, height, playerPos, minimumRadiusDistance):
    x = random.randint(0, width-1)
    minY = 0

    if abs(x - playerPos[0]) < minimumRadiusDistance:
        minY = playerPos[1] + minimumRadiusDistance
    y = random.randint(minY, height-1)

    return (x,y)

# Stress-test:

def stressTest():
    uniquePlayerPositions = {}
    uniqueValidPositions = {}
    
    for i in range(100000):
        width = 25
        height = 25
        minimumDistance = 2
        playerPos = (random.randint(0, width-1), 0)
    
        pos = getValidPosition(width, height, playerPos, minimumDistance)
        uniquePlayerPositions[playerPos] = 1
        uniqueValidPositions[pos] = 1
    
        if (pos[0] >= width):
            print("* * * INVALID X")
            print("\nPlayer Position:\t", playerPos)
            print("Valid Position:\t\t", pos)
            quit()
        if (pos[1] >= height):
            print("* * * INVALID Y")
            print("\nPlayer Position:\t", playerPos)
            print("Valid Position:\t\t", pos)
            quit()
        if (abs(pos[0] - playerPos[0]) < minimumDistance) and (abs(pos[1] - playerPos[1]) < minimumDistance):
            print("* * * INVALID POS (TOO CLOSE TO PLAYER)")
            print("\nPlayer Position:\t", playerPos)
            print("Valid Position:\t\t", pos)
            quit()
            
    # Validate expectations
    
    try:
        assert(len(uniquePlayerPositions.keys()) == width)
        print("Check OK: {0} == {1}".format(len(uniquePlayerPositions.keys()), width))
    except:
        print("Exception: {0} != {1}".format(len(uniquePlayerPositions.keys()), width))
    
    try:
        assert(len(uniqueValidPositions.keys()) == width)
        print("Check OK: {0} == {1}".format(len(uniqueValidPositions.keys()), width*height))
    except:
        print("Exception: {0} != {1}".format(len(uniqueValidPositions.keys()), width*height))

if __name__ == "__main__":
    stressTest()