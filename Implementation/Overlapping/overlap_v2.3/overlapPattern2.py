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
def drawPattern2(overlapNode, remainNodes):
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
        rotateAngle = rotateRate * i
        drawArcCombo(center, radius, rotateAngle, node, ax1)

        rectLength = node.getNodeWidth()
        thisDots = drawPoint(node, ax1)

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

# !!! Additional speration of overlapped part and remaining part is NEEDED !!!
overlapNode = OverlapNode("CD_FGHI_KLMN")
overlapPart = Node("AB")

# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,9))
f.subplots_adjust(hspace=0,wspace=0)

drawPattern2(overlapPart, overlapNode)

# Specify the axis settings
plt.grid(True)
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)

plt.show()