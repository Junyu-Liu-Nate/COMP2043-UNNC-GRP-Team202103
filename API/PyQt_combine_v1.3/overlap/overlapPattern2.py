#-- Overlap Pattern 2 - Using circle as overlapped areas --#

from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

from node import Node
from overlapNode import OverlapNode

from overlapDraw import drawLiteral
from overlapDraw import drawPoint
from overlapDraw import drawArcCombo

# 2nd Design Pattern - Use circles to highlight the overlapped literals
# Draw final image (currently including draw edge connections)
def drawPattern2(overlapNode, remainNodes, startAngle):
    drawLiteral(overlapNode)

    nodeList = remainNodes.getNodesContain()
    center = remainNodes.getCenter()
    nodeNum = remainNodes.getNodeNum()
    rotateRate = 360 / nodeNum

    i = 0
    centers = []
    radius = 0.7

    for node in nodeList:
        radius = radius + 0.15
        rotateAngle = startAngle + rotateRate * i
        drawArcCombo(center, radius, rotateAngle, node, ax1)

        rectLength = node.getNodeWidth()
        drawPoint(node, ax1)

        # if (i < len(remainLiteralList) - 1):
        #     nextLiterals = remainLiteralList[i+1]
        #     literalNum2 = len(nextLiterals)
        #     intervalNum2 = literalNum2 - 1
        #     literalsLengthHalf2 = intervalNum2 * literalWidth * 4
        #     rectLength2 = literalsLengthHalf2 + 2
        #     calLength2 = radius + 0.15 + rectLength2 / 2
        #     rotateAngle2 = rotateRate * (i + 1)
        #     centers2 = [center[0] + calLength2 * math.cos(math.radians(rotateAngle2)), center[1] + calLength2 * math.sin(math.radians(rotateAngle2))]
        #     nextDots = drawDot(remainLiteralList[i + 1], centers2, rotateAngle2, plt)
        #     plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])
        # else:
        #     nextLiterals = remainLiteralList[0]
        #     literalNum2 = len(nextLiterals)
        #     intervalNum2 = literalNum2 - 1
        #     literalsLengthHalf2 = intervalNum2 * literalWidth * 4
        #     rectLength2 = literalsLengthHalf2 + 2
        #     calLength2 = 0.85 + rectLength2 / 2 # ??? 0.85 still need to be justified
        #     rotateAngle2 = rotateRate * (i + 1)
        #     centers2 = [center[0] + calLength2 * math.cos(math.radians(rotateAngle2)), center[1] + calLength2 * math.sin(math.radians(rotateAngle2))]
        #     nextDots = drawDot(remainLiteralList[0], centers2, rotateAngle2, plt)
        #     plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])

        i = i + 1

#----- Calculate Drawing Settings -----#
# !!! Additional speration of overlapped part and remaining part is NEEDED !!!
overlapNode1 = OverlapNode("CDEF_FGHI_KLMN")
overlapPart1 = Node("AB")

overlapNode2 = OverlapNode("FEDC_ISJND_KSIDD")
overlapPart2 = Node("GH")

# !!! This is only a brief demo. More generalized layout calculation should be implemented here !!!
tempNode = overlapNode1.findSubNode("CDEF")
tempNodeWidth = tempNode.getNodeWidth()
tempNodeHeight = tempNode.getNodeHeight()
tempNodeAngle = tempNode.getAngle()

# !!! This is just a demonstration of the 1st layer (inner most circle) !!!
currentRadius = 0.7 + 0.15
centerDistance = math.sqrt(currentRadius * currentRadius - tempNodeHeight * tempNodeHeight / 4) * 2 + tempNodeWidth

overlapNode1Center = overlapNode1.getCenter()
overlapNode2.setxCenter(overlapNode1Center[0] + centerDistance * math.cos(math.radians(tempNodeAngle)))
overlapNode2.setyCenter(overlapNode1Center[1] + centerDistance * math.sin(math.radians(tempNodeAngle)))
overlapPart2.adjustX(centerDistance * math.cos(math.radians(tempNodeAngle)))
overlapPart2.adjustY(centerDistance * math.sin(math.radians(tempNodeAngle)))


#----- Draw Graph -----#
# # Specify the size of figure window
# f,(ax1) = plt.subplots(1,1,figsize=(10,9))
# f.subplots_adjust(hspace=0,wspace=0)

# drawPattern2(overlapPart1, overlapNode1, 0)
# drawPattern2(overlapPart2, overlapNode2, tempNodeAngle - 180)

# # Specify the axis settings
# plt.grid(True)
# ax1.set_xlim(-6,6)
# ax1.set_ylim(-6,6)

# plt.show()