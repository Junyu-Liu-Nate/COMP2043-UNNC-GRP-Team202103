#-- Overlap Pattern 1 --#

from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np

from node import Node
from overlapNode import OverlapNode
# from graph import Graph

from overlapDraw import drawLiteral
from overlapDraw import drawPoint
from overlapDraw import drawRectangle
from overlapPattern2 import drawPattern2

# 1st Design Pattern - supernodes overlap on each other directly
# Draw final image (currently including draw edge connections)
def drawPattern1(overlapNode, startAngle):
    nodeList = overlapNode.getNodesContain()
    center = overlapNode.getCenter()
    nodeNum = overlapNode.getNodeNum()
    rotateRate = 360 / nodeNum
    
    i = 0
    centers = []
    for node in nodeList:
        literalsLengthHalf = node.getLiteralsLength() / 2
        rotateAngle = startAngle + rotateRate * i
        node.setAngle(rotateAngle)
        nodeCenter = [center[0] + literalsLengthHalf * math.cos(math.radians(rotateAngle)), center[1] + literalsLengthHalf * math.sin(math.radians(rotateAngle))]
        node.adjustX(nodeCenter[0])
        node.adjustY(nodeCenter[1])

        drawLiteral(node)
        drawRectangle(node, ax1)
        drawPoint(node, ax1)

        # if (i < nodeNum - 1):
        #     nextLiterals = literalList[i+1]
        #     literalNum2 = len(nextLiterals)
        #     intervalNum2 = literalNum2 - 1
        #     literalsLengthHalf2 = intervalNum2 * literalWidth * 2
        #     rotateAngle2 = rotateRate * (i + 1)
        #     centers2 = [center[0] + literalsLengthHalf2 * math.cos(math.radians(rotateAngle2)), center[1] + literalsLengthHalf2 * math.sin(math.radians(rotateAngle2))]
        #     nextDots = drawDot(literalsList[i + 1], centers2, rotateAngle2, plt)
        #     plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])
        # else:
        #     nextLiterals = literalList[0]
        #     literalNum2 = len(nextLiterals)
        #     intervalNum2 = literalNum2 - 1
        #     literalsLengthHalf2 = intervalNum2 * literalWidth * 2
        #     rotateAngle2 = rotateRate * (i + 1)
        #     centers2 = [center[0] + literalsLengthHalf2 * math.cos(math.radians(rotateAngle2)), center[1] + literalsLengthHalf2 * math.sin(math.radians(rotateAngle2))]
        #     nextDots = drawDot(literalsList[0], centers2, rotateAngle2, plt)
        #     plt.plot([thisDots[1][0], nextDots[0][0]], [thisDots[1][1], nextDots[0][1]])

        i = i + 1

#----- Calculate Drawing Settings -----#
# !!! A new layout algorithm should be implemented here !!!
overlapNode1 = OverlapNode("ABCD_AEFGHI_AJKLMN_AQW_AYUIW")
overlapNode2 = OverlapNode("DCBA_DOLK_DINXSV_DOPI_DYSU")

# !!! This is only a brief demo. More generalized layout calculation should be implemented here !!!
tempNode = overlapNode1.findSubNode("ABCD")
# tempNodeCenter = [tempNode.getXAnchor(), tempNode.getYAnchor()]
tempNodeEnd2 = tempNode.getEnd2Coordinate()
overlapNode2.setxCenter(tempNodeEnd2[0])
overlapNode2.setyCenter(tempNodeEnd2[1])
tempNodeAngle = tempNode.getAngle()

#----- Draw Graph -----#
# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,9))
f.subplots_adjust(hspace=0,wspace=0)

# Draw grpah
drawPattern1(overlapNode1, 0)
drawPattern1(overlapNode2, tempNodeAngle - 180)

# Specify the axis settings
plt.grid(True)
ax1.set_xlim(-6,6)
ax1.set_ylim(-6,6)

plt.show()