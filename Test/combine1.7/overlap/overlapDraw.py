#-- Basic drawing functions --#
from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

from node import Node
from overlapNode import OverlapNode

#----- Settings of literal sizes -----#
#----- Current setting is based on fontsize 16 -----#
literalWidth = 0.18
literalHeight = 0.3
literalInterval = 0.18
horizonMargin = 0.05
verticalMargin = 0.1
horizonMove = 0.09
verticalMove = 0.15
first = True
num = False
onesDigit = False
tensDigit = False

def drawLiteralOriginal(node):
    """
    Original drawing function of literals
    :param node: stands for a node object
    :return: no return
    """
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
    drawLiterals.pop(len(drawLiterals) - 1)
    
    # Draw literals one by one along the rotateAngle
    for i in drawLiterals:
        plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize = 4.8)
        drawPosition = [drawPosition[0] + (literalInterval*2) * math.cos(math.radians(rotateAngle)), drawPosition[1] + (literalInterval*2) * math.sin(math.radians(rotateAngle))]

def drawLiteral(node, zoomratio):
    """
    More complex drawing function of literals
    Note that [-6,-6] corresponds to font size 16; and the ratio of main character and suffix is 1.6:1
    :param node: stands for a node object
    :param zoomratio: stands for the zoom ratio of the draw literals
    :return: no return
    """
    global num, onesDigit, tensDigit;  # check one digit or two digits
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
    drawLiterals.pop(len(drawLiterals) - 1)
    onesDigit = False
    tensDigit = False
    
    # Draw literals one by one along the rotateAngle
    for i in drawLiterals:
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
                drawPosition[0]-=0.12
            elif(tensDigit):
                drawPosition[0]-=0.17
            drawPosition = [drawPosition[0] + (literalInterval * 2) * math.cos(math.radians(rotateAngle)),drawPosition[1] + (literalInterval * 2) * math.sin(math.radians(rotateAngle))]
            plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize=16 / zoomratio)
            onesDigit = False
            tensDigit = False
        else:
            if (num):
                drawPosition = bridgePosition2
                tensDigit = True
                num = False
            else:
                drawPosition = bridgePosition1
                onesDigit = True
            num = True
            plt.text(drawPosition[0] - horizonMove, drawPosition[1] - verticalMove, i, fontsize=10 / zoomratio)
    first = True

def drawRectangle(node, axis):
    """
    Drawing function of a rectangle cover
    :param node: stands for a node object
    :param axis: stands for an axis to be drawn
    :return: no return
    """
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

def drawPoint(node, axis):
    """
    Drawing function of a point
    :param node: stands for a node object
    :param axis: stands for an axis to be drawn
    :return: no return
    """
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

def drawEdge(node1, node2):
    """
    Drawing function of an edge
    Automatic connect the nearest two points to avoid edge-node crossover.
    :param node1: stand for the nodes which this edge connect
    :param node2: stand for the nodes which this edge connect
    :return: no return
    """
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

def drawArc(center, radius, rotateAngle, axis):
    """
    Drawing function of an Arc
    :param center: stands for the circle center from which the Arc is drawn
    :param radius: stands for the circle radius from which the Arc is drawn
    :param rotateAngle: stands for the circle radius from which the Arc is drawn
    :param axis: stands for the axis where the Arc is drawn
    :return: no return
    """
    halfRecHeight = 0.25
    halfSectorAngle = np.arcsin(halfRecHeight / radius)
    #print(halfSectorAngle)
    halfSectorAngle = math.degrees(halfSectorAngle)
    sectorAngle = halfSectorAngle * 2
    startAngle = rotateAngle - halfSectorAngle
    endAngle = rotateAngle + halfSectorAngle
    arc1 = matplotlib.patches.Arc(center, radius * 2, radius * 2, theta1 = endAngle, theta2 = startAngle, color = "black")
    axis.add_patch(arc1)

def drawArcCombo(center, radius, rotateAngle, node, axis, zoomRatio):
    """
    Drawing function of an Arc and rectangle combination
    :param center: stands for the circle center from which the Arc and rectangle combination is drawn
    :param radius: radius stands for the circle radius from which the Arc is drawn
    :param rotateAngle: rotateAngle stands for the circle radius from which the Arc is drawn
    :param node: stands for a node object
    :param axis: stands for the axis where the Arc is drawn
    :param zoomRatio: stands for the zoom ratio of the literals to be drawn
    :return: no return
    """
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

def calDistance(point1, point2):
    """
    Calculate the distance bewteen two points
    :param point1: the coordiante of point 1
    :param point2: the coordiante of point 2
    :return: a number which stands for the distance between two points
    """
    distance = math.sqrt((point1[0]-point2[0]) * (point1[0]-point2[0]) + (point1[1]-point2[1]) * (point1[1]-point2[1]))
    return distance