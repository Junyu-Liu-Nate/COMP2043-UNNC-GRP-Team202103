import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

# 
literalWidth = 0.18
literalHeight = 0.3
literalInterval = 0.18
horizonMargin = 0.05
verticalMargin = 0.1
horizonMove = 0.09
verticalMove = 0.15

def drawLiteral(literals, center, rotateAngle, plt):
    #literals.replace("_", "")
    literalNum = len(literals)
    intervalNum = literalNum - 1
    literalsLength = intervalNum * literalWidth * 4
    drawPosition = [center[0] - literalsLength / 2 * math.cos(math.radians(rotateAngle)), center[1] - literalsLength / 2 * math.sin(math.radians(rotateAngle))]
    
    drawLiterals = []
    for i in literals:
        drawLiterals.append(i)
        drawLiterals.append(" ")
    drawLiterals.pop(len(drawLiterals) - 1)
    # print(drawLiterals)

    for i in drawLiterals:
        plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize = 16)
        drawPosition = [drawPosition[0] + (literalInterval*2) * math.cos(math.radians(rotateAngle)), drawPosition[1] + (literalInterval*2) * math.sin(math.radians(rotateAngle))]

def drawRectangle(literals, centerR, rotateAngle, plt):
    literalNum = len(literals)
    intervalNum = literalNum - 1
    literalsLength = intervalNum * literalWidth * 4

    rectLength = literalsLength + 0.5
    rectTheta = np.arctan(0.25 / rectLength / 2)
    rectTheta = np.degrees(rectTheta)
    calTheta = rectTheta + rotateAngle
    calLength = math.sqrt(0.25 * 0.25 + (rectLength / 2) * (rectLength / 2))

    #drawPosition = [center[0] - calLength * math.cos(math.radians(calTheta)), center[1] - calLength * math.sin(math.radians(calTheta))]
    #drawPosition = [center[0] - literalsLength / 2 * math.cos(math.radians(rotateAngle)) - 0.1, center[1] - literalsLength / 2 * math.sin(math.radians(rotateAngle)) - 0.1]
    #rec = mPatches.Rectangle((drawPosition[0], drawPosition[1]), rectLength, 0.5, angle = rotateAngle, facecolor = "none")
    #print(centerR)
    ts = ax1.transData
    tr = matplotlib.transforms.Affine2D().rotate_deg_around(centerR[0],centerR[1], rotateAngle)
    t = tr + ts
    rect1 = matplotlib.patches.Rectangle((centerR[0] - rectLength / 2, centerR[1]-0.25),rectLength,0.5,linewidth=1,facecolor='none',transform=t)
    ax1.add_patch(rect1)

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
        i = i + 1
    #return centers


literalsList = ["ABC", "ADEF", "AGHIJK", "ASISO", "ASDHD"]
center = [0, 0]
# centersList = calPosition(literalsList, center)

# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,8))
f.subplots_adjust(hspace=0,wspace=0)

# Specify the rotation settings
# ts = ax1.transData
# coords = [1,0]
# tr = matplotlib.transforms.Affine2D().rotate_deg_around(coords[0],coords[1], 10)
# t = tr + ts

#rec0 = matplotlib.patches.Rectangle((-1,-0.5),1,0.5,linewidth=1,edgecolor='r',facecolor='none')
#ax1.add_patch(rec0)
#Rotated rectangle patch
#rect1 = matplotlib.patches.Rectangle((0,-1),2,2,linewidth=1,edgecolor='b',facecolor='none',transform=t)
#ax1.add_patch(rect1)

#plt.text(-0.95, -0.4, literals[0], fontsize = 16)
# drawLiteral("ABCD", [0,0], 60, plt)
# drawRectangle("ABCD", [0,0], 60, plt)
# drawLiteral("AEFGH", [0,0], 120, plt)
# drawRectangle("AEFGH", [0,0], 120, plt)

# literalsNum = len(literalsList)
# rotateRate = 360 / literalsNum
# i = 0
# for center in centersList:
#     rotateAngle = rotateRate * i
#     drawLiteral(literalsList[i], center, rotateAngle, plt)
#     drawRectangle(literalsList[i], center, rotateAngle, plt)
#     i = i + 1

draw(literalsList, center)

# Specify the axis settings
plt.grid(True)
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)

plt.show()