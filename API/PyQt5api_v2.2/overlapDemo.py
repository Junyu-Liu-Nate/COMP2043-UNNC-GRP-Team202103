from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

# Settings of literal sizes
# !!! Current setting is based on fontsize 16 !!!
from PyQt5 import QtGui

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
    rectLength = literalsLength + 2

    ts = ax1.transData
    tr = matplotlib.transforms.Affine2D().rotate_deg_around(centerR[0],centerR[1], rotateAngle)
    t = tr + ts
    rect1 = matplotlib.patches.Rectangle((centerR[0] - rectLength / 2, centerR[1]-0.25),rectLength,0.5,linewidth=1,edgecolor='black',facecolor='none',transform=t)
    ax1.add_patch(rect1)

# Draw connection points of a supernode around center coordinates
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

#----------------------------------------------------------------------------------------------
def drawArc(center, radius, rotateAngle):
    halfRecHeight = 0.25
    halfSectorAngle = np.arcsin(halfRecHeight / radius)
    #print(halfSectorAngle)
    halfSectorAngle = math.degrees(halfSectorAngle)
    sectorAngle = halfSectorAngle * 2
    startAngle = rotateAngle - halfSectorAngle
    endAngle = rotateAngle + halfSectorAngle
    arc1 = matplotlib.patches.Arc(center, radius * 2, radius * 2, theta1 = endAngle, theta2 = startAngle, color = "black")
    ax1.add_patch(arc1)

def drawArcCombo(center, radius, rotateAngle, remainLiterals):
    literalNum = len(remainLiterals)
    intervalNum = literalNum - 1
    # !!! The current setting of length calculation is adding 2 spaces between two letters !!!
    literalsLength = intervalNum * literalWidth * 4
    # rectLength = literalsLength + 0.5
    rectLength = literalsLength + 2
    
    halfRecHeight = 0.25
    halfSectorAngle = np.arcsin(halfRecHeight / radius)
    calLength = radius * math.cos(halfSectorAngle) + rectLength / 2
    centerR = [center[0] + calLength * math.cos(math.radians(rotateAngle)), center[1] + calLength * math.sin(math.radians(rotateAngle))]
    drawLiteral(remainLiterals, centerR, rotateAngle, plt)
    drawRectangle(remainLiterals, centerR, rotateAngle, plt)
    drawArc(center, radius, rotateAngle)
    
    calGamma = np.arctan(0.38 / rectLength) # !!!
    # print(calGamma)
    calGamma = math.degrees(calGamma)
    callength2 = math.sqrt(0.25*0.25 + (rectLength / 2) * (rectLength / 2))
    calAngle1 = rotateAngle + calGamma
    calAngle2 = rotateAngle - calGamma
    point1 = [centerR[0] - callength2 * math.cos(math.radians(calAngle1)), centerR[1] - callength2 * math.sin(math.radians(calAngle1))]
    point2 = [centerR[0] - callength2 * math.cos(math.radians(calAngle2)), centerR[1] - callength2 * math.sin(math.radians(calAngle2))]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], linewidth = 4, color = "white")

def drawPattern2(overlapLiterals, remainLiteralList, center):
    drawLiteral(overlapLiterals, center, 0, plt)

    literalsNum = len(remainLiteralList)
    rotateRate = 360 / literalsNum
    i = 0
    centers = []
    radius = 0.7

    for remainLiterals in remainLiteralList:
        radius = radius + 0.15
        rotateAngle = rotateRate * i
        drawArcCombo(center, radius, rotateAngle, remainLiterals)

        literalNum = len(remainLiterals)
        intervalNum = literalNum - 1
        literalsLength = intervalNum * literalWidth * 4
        rectLength = literalsLength + 2
    
        halfRecHeight = 0.25
        halfSectorAngle = np.arcsin(halfRecHeight / radius)
        calLength = radius * math.cos(halfSectorAngle) + rectLength / 2
        centerR = [center[0] + calLength * math.cos(math.radians(rotateAngle)), center[1] + calLength * math.sin(math.radians(rotateAngle))]
        thisDots = drawDot(remainLiterals, centerR, rotateAngle, plt)

        if (i < len(remainLiteralList) - 1):
            nextLiterals = remainLiteralList[i+1]
            literalNum2 = len(nextLiterals)
            intervalNum2 = literalNum2 - 1
            literalsLengthHalf2 = intervalNum2 * literalWidth * 4
            rectLength2 = literalsLengthHalf2 + 2
            calLength2 = radius + 0.15 + rectLength2 / 2
            rotateAngle2 = rotateRate * (i + 1)
            centers2 = [center[0] + calLength2 * math.cos(math.radians(rotateAngle2)), center[1] + calLength2 * math.sin(math.radians(rotateAngle2))]
            nextDots = drawDot(remainLiteralList[i + 1], centers2, rotateAngle2, plt)
            plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])
        else:
            nextLiterals = remainLiteralList[0]
            literalNum2 = len(nextLiterals)
            intervalNum2 = literalNum2 - 1
            literalsLengthHalf2 = intervalNum2 * literalWidth * 4
            rectLength2 = literalsLengthHalf2 + 2
            calLength2 = 0.85 + rectLength2 / 2 # ??? 0.85 still need to be justified
            rotateAngle2 = rotateRate * (i + 1)
            centers2 = [center[0] + calLength2 * math.cos(math.radians(rotateAngle2)), center[1] + calLength2 * math.sin(math.radians(rotateAngle2))]
            nextDots = drawDot(remainLiteralList[0], centers2, rotateAngle2, plt)
            plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])

        i = i + 1


# Draw final image (including draw edge connections)
def drawPattern1(literalList, center):
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
    # return centers


literalsList = ["ABC", "ADEF", "AGHIJK", "ASISO", "ASDHD"]
literalsList2 = ["CD", "DEFP", "GHIJK", "SISO", "SDHD"]
center = [0, 0]

# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,9))
f.subplots_adjust(hspace=0,wspace=0)

# drawPattern1(literalsList, center)
drawPattern2("AB", literalsList2, center)


# Specify the axis settings
plt.grid(True)
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)

from PyQt5.QtGui import *

# img = QtGui.QImage(ax1, 12, 12, QtGui.QImage.Format_Indexed8)
# plot = ax1.plot()
# img = plt.gcf()
# img.savefig("overlapped.png")



# plt.show()