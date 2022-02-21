import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

# Settings of literal sizes
# !!! Current setting is based on fontsize 16 !!!
literalWidth = 0.18
literalHeight = 0.3
literalInterval = 0.18
horizonMargin = 0.05
verticalMargin = 0.1
horizonMove = 0.09
verticalMove = 0.15

# Draw literals of a supernode around center coordinates
def drawLiteral(literals, center, rotateAngle, plt):
    literalNum = len(literals)
    intervalNum = literalNum - 1
    # !!! The current setting of length calculation is adding 2 spaces between two letters !!!
    literalsLength = intervalNum * literalWidth * 4
    drawPosition = [center[0] - literalsLength / 2 * math.cos(math.radians(rotateAngle)), center[1] - literalsLength / 2 * math.sin(math.radians(rotateAngle))]
    
    drawLiterals = []
    for i in literals:
        drawLiterals.append(i)
        drawLiterals.append(" ")
    drawLiterals.pop(len(drawLiterals) - 1)

    for i in drawLiterals:
        plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize = 16)
        drawPosition = [drawPosition[0] + (literalInterval*2) * math.cos(math.radians(rotateAngle)), drawPosition[1] + (literalInterval*2) * math.sin(math.radians(rotateAngle))]

# Draw rectangle cover of a supernode around center coordinates
def drawRectangle(literals, centerR, rotateAngle, plt):
    literalNum = len(literals)
    intervalNum = literalNum - 1
    # !!! The current setting of length calculation is adding 2 spaces between two letters !!!
    literalsLength = intervalNum * literalWidth * 4

    rectLength = literalsLength + 0.5

    ts = ax1.transData
    tr = matplotlib.transforms.Affine2D().rotate_deg_around(centerR[0],centerR[1], rotateAngle)
    t = tr + ts
    rect1 = matplotlib.patches.Rectangle((centerR[0] - rectLength / 2, centerR[1]-0.25),rectLength,0.5,linewidth=1,edgecolor='black',facecolor='none',transform=t)
    ax1.add_patch(rect1)

# Draw connection ponits of a supernode around center coordinates
def drawDot(literals, center, rotateAngle, plt):
    horizontalShift = 0.25 * math.sin(math.radians(rotateAngle))
    verticalShift = 0.25 * math.cos(math.radians(rotateAngle))
    dot1Center = [center[0] + horizontalShift, center[1] - verticalShift]
    circle1 = plt.Circle((dot1Center[0], dot1Center[1]), 0.05)
    dot2Center = [center[0] - horizontalShift, center[1] + verticalShift]
    circle2 = plt.Circle((dot2Center[0], dot2Center[1]), 0.05)
    ax1.add_patch(circle1)
    ax1.add_patch(circle2)

    dots = [dot1Center, dot2Center]
    return dots

# Draw final image (including draw edge connections)
def draw(literalList, center):
    literalsNum = len(literalList)
    rotateRate = 360 / literalsNum
    i = 0
    centers = []
    for literals in literalList:
        literalNum = len(literals)
        intervalNum = literalNum - 1
        literalsLengthHalf = intervalNum * literalWidth * 2
        rotateAngle = rotateRate * i
        #centers.append([center + literalsLengthHalf * math.cos(math.radians(rotateAngle)), center + literalsLengthHalf * math.sin(math.radians(rotateAngle))])
        centers = [center[0] + literalsLengthHalf * math.cos(math.radians(rotateAngle)), center[1] + literalsLengthHalf * math.sin(math.radians(rotateAngle))]
        drawLiteral(literalsList[i], centers, rotateAngle, plt)
        drawRectangle(literalsList[i], centers, rotateAngle, plt)
        thisDots = drawDot(literalsList[i], centers, rotateAngle, plt)

        if (i < len(literalList) - 1):
            nextLiterals = literalList[i+1]
            literalNum2 = len(nextLiterals)
            intervalNum2 = literalNum2 - 1
            literalsLengthHalf2 = intervalNum2 * literalWidth * 2
            rotateAngle2 = rotateRate * (i + 1)
            centers2 = [center[0] + literalsLengthHalf2 * math.cos(math.radians(rotateAngle2)), center[1] + literalsLengthHalf2 * math.sin(math.radians(rotateAngle2))]
            nextDots = drawDot(literalsList[i + 1], centers2, rotateAngle2, plt)
            plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])
        else:
            nextLiterals = literalList[0]
            literalNum2 = len(nextLiterals)
            intervalNum2 = literalNum2 - 1
            literalsLengthHalf2 = intervalNum2 * literalWidth * 2
            rotateAngle2 = rotateRate * (i + 1)
            centers2 = [center[0] + literalsLengthHalf2 * math.cos(math.radians(rotateAngle2)), center[1] + literalsLengthHalf2 * math.sin(math.radians(rotateAngle2))]
            nextDots = drawDot(literalsList[0], centers2, rotateAngle2, plt)
            plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])

        i = i + 1
    #return centers


literalsList = ["ABC", "ADEF", "AGHIJK", "ASISO", "ASDHD"]
center = [0, 0]

# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,8))
f.subplots_adjust(hspace=0,wspace=0)

draw(literalsList, center)

# Specify the axis settings
plt.grid(True)
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)

plt.show()