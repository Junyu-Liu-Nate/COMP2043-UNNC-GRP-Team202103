#-- Basic drawing functions --#

from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

from node import Node
from overlapNode import OverlapNode

#-- Settings of literal sizes --#
# !!! Current setting is based on fontsize 16 !!!
literalWidth = 0.18
literalHeight = 0.3
literalInterval = 0.18
horizonMargin = 0.05
verticalMargin = 0.1
horizonMove = 0.09
verticalMove = 0.15
first = True;
num = False;
onesDigit = False;
tensDigit = False;

# # Draw Literals
# def drawLiteral(node):
#     literals = node.getName()
#     literalsLength = node.getLiteralsLength()
#     centerX = node.getXAnchor()
#     centerY = node.getYAnchor()
#     rotateAngle = node.getAngle()

#     # Calculate the draw position of the 1st literal
#     drawPosition = [centerX - literalsLength / 2 * math.cos(math.radians(rotateAngle)), centerY - literalsLength / 2 * math.sin(math.radians(rotateAngle))]

#     # Insert blank spaces as intervals
#     drawLiterals = []
#     for i in literals:
#         drawLiterals.append(i)
#         drawLiterals.append(" ")
#     drawLiterals.pop(len(drawLiterals) - 1)
    
#     # Draw literals one by one along the rotateAngle
#     for i in drawLiterals:
#         plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize = 4.8)
#         drawPosition = [drawPosition[0] + (literalInterval*2) * math.cos(math.radians(rotateAngle)), drawPosition[1] + (literalInterval*2) * math.sin(math.radians(rotateAngle))]

# Draw Literals
# Note that [-6,-6] corresponds to font size 16; and the ratio of main character and suffix is 1.6:1
def drawLiteral(node, zoomratio):
    literals = node.getName()
    literalsLength = node.getLiteralsLength()
    centerX = node.getXAnchor()
    centerY = node.getYAnchor()
    rotateAngle = node.getAngle()

    # Calculate the draw position of the 1st literal
    drawPosition = [centerX - literalsLength / 2 * math.cos(math.radians(rotateAngle)), centerY - literalsLength / 2 * math.sin(math.radians(rotateAngle))]
    # Insert blank spaces as intervals
    drawLiterals = []
    for i in literals:
        drawLiterals.append(i)
        drawLiterals.append(" ")
    # print(drawLiterals)
    drawLiterals.pop(len(drawLiterals) - 1)
    
    # Draw literals one by one along the rotateAngle
    for i in drawLiterals:
        global num, onesDigit, tensDigit; # check one digit or two digits
        if(i.isalpha()):
            global first;   # the position is calculated at the first time so no need to calculate again.
            if(not first):
                drawPosition = [drawPosition[0] + (literalInterval * 2) * math.cos(math.radians(rotateAngle)), drawPosition[1] + (literalInterval * 2) * math.sin(math.radians(rotateAngle))]
            bridgePosition1 = [drawPosition[0] + 0.12, drawPosition[1]]
            bridgePosition2 = [drawPosition[0] + 0.17, drawPosition[1]]
            plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize= 16 / zoomratio)
            first = False;
            num = False;
        elif(i.isspace()):
            # move the x coordinate to the previous one
            if(onesDigit):
                drawPosition[0]-=0.12;
            elif(tensDigit):
                drawPosition[0]-=0.17;
            drawPosition = [drawPosition[0] + (literalInterval * 2) * math.cos(math.radians(rotateAngle)),drawPosition[1] + (literalInterval * 2) * math.sin(math.radians(rotateAngle))]
            plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize=16 / zoomratio)
            onesDigit = False;
            tensDigit = False;
        else:
            if (num):
                drawPosition = bridgePosition2;
                tensDigit = True;
                num = False;
            else:
                drawPosition = bridgePosition1;
                onesDigit = True;
            num = True;
            plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize=10 / zoomratio)
    first = True;

# Draw Rectangle Cover
def drawRectangle(node, axis):
    nodeWidth = node.getNodeWidth()
    nodeHeight = node.getNodeHeight()
    centerX = node.getXAnchor()
    centerY = node.getYAnchor()
    rotateAngle = node.getAngle()

    ts = axis.transData
    tr = matplotlib.transforms.Affine2D().rotate_deg_around(centerX,centerY, rotateAngle)
    t = tr + ts
    rect1 = matplotlib.patches.Rectangle((centerX - nodeWidth / 2, centerY-0.25),nodeWidth,nodeHeight,linewidth=1,edgecolor='black',facecolor='none',transform=t)
    axis.add_patch(rect1)

# Draw Point
def drawPoint(node, axis):
    centerX = node.getXAnchor()
    centerY = node.getYAnchor()
    rotateAngle = node.getAngle()

    horizontalShift = 0.25 * math.sin(math.radians(rotateAngle))
    verticalShift = 0.25 * math.cos(math.radians(rotateAngle))

    # This calculation should be move into Node class ???
    point1Center = [centerX + horizontalShift, centerY - verticalShift]
    node.setConnectPonit1(point1Center)
    circle1 = plt.Circle((point1Center[0], point1Center[1]), 0.05)
    point2Center = [centerX - horizontalShift, centerY + verticalShift]
    node.setConnectPonit2(point2Center)
    circle2 = plt.Circle((point2Center[0], point2Center[1]), 0.05)
    axis.add_patch(circle1)
    axis.add_patch(circle2)

    # pointCenters = [point1Center, point1Center]
    # return pointCenters

# Draw edges
# Automatic connect the nearest two points to avoid edge-node crossover.
def drawEdge(node1, node2):
    pointList = []
    pointList.append(node1.getConnectPoint1())
    pointList.append(node1.getConnectPoint2())
    pointList.append(node2.getConnectPoint1())
    pointList.append(node2.getConnectPoint2())

    pointPairList = []
    pointPairList.append([pointList[0], pointList[2]])
    pointPairList.append([pointList[0], pointList[3]])
    pointPairList.append([pointList[1], pointList[2]])
    pointPairList.append([pointList[1], pointList[3]])

    distanceList = []
    for pointPair in pointPairList:
        distanceList.append(calDistance(pointPair[0], pointPair[1]))
    
    minIndex = distanceList.index(min(distanceList))
    drawPointPair = pointPairList[minIndex]

    plt.plot([drawPointPair[0][0], drawPointPair[1][0]], [drawPointPair[0][1], drawPointPair[1][1]])

# Draw arc
def drawArc(center, radius, rotateAngle, axis):
    halfRecHeight = 0.25
    halfSectorAngle = np.arcsin(halfRecHeight / radius)
    #print(halfSectorAngle)
    halfSectorAngle = math.degrees(halfSectorAngle)
    sectorAngle = halfSectorAngle * 2
    startAngle = rotateAngle - halfSectorAngle
    endAngle = rotateAngle + halfSectorAngle
    arc1 = matplotlib.patches.Arc(center, radius * 2, radius * 2, theta1 = endAngle, theta2 = startAngle, color = "black")
    axis.add_patch(arc1)

# Draw arcs and rectangles combination
def drawArcCombo(center, radius, rotateAngle, node, axis, zoomRatio):
    rectLength = node.getNodeWidth()
    
    halfRecHeight = 0.25
    halfSectorAngle = np.arcsin(halfRecHeight / radius)
    calLength = radius * math.cos(halfSectorAngle) + rectLength / 2
    nodeCenter = [center[0] + calLength * math.cos(math.radians(rotateAngle)), center[1] + calLength * math.sin(math.radians(rotateAngle))]
    # node.adjustX(nodeCenter[0])
    # node.adjustY(nodeCenter[1])
    # node.setAngle(rotateAngle)
    drawLiteral(node, zoomRatio)
    drawRectangle(node, axis)
    drawArc(center, radius, rotateAngle, axis)
    
    calGamma = np.arctan(0.38 / rectLength) # !!!
    calGamma = math.degrees(calGamma)
    callength2 = math.sqrt(0.25*0.25 + (rectLength / 2) * (rectLength / 2))
    calAngle1 = rotateAngle + calGamma
    calAngle2 = rotateAngle - calGamma
    point1 = [nodeCenter[0] - callength2 * math.cos(math.radians(calAngle1)), nodeCenter[1] - callength2 * math.sin(math.radians(calAngle1))]
    point2 = [nodeCenter[0] - callength2 * math.cos(math.radians(calAngle2)), nodeCenter[1] - callength2 * math.sin(math.radians(calAngle2))]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], linewidth = 4, color = "white")

#--- Helper functions ---#
# Calculate the distance of two points
def calDistance(point1, point2):
    # distance = math.sqrt((point1[0]-point2[0]) ^ 2 + (point1[1]-point2[1]) ^ 2)
    distance = math.sqrt((point1[0]-point2[0]) * (point1[0]-point2[0]) + (point1[1]-point2[1]) * (point1[1]-point2[1]))
    return distance