#-- Overlap Pattern 1 --#

from turtle import circle
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mPatches
import numpy as np
from layoutAlgorithmOriginal import calLayout

from node import Node
from overlapNode import OverlapNode
from graph import Graph

from overlapDraw import drawEdge, drawLiteral
from overlapDraw import drawPoint
from overlapDraw import drawRectangle
from overlapPattern2 import drawPattern2

# 1st Design Pattern - supernodes overlap on each other directly
# Draw final image (currently including draw edge connections)
def drawPattern1(overlapNode, startAngle, axis):
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
        drawRectangle(node, axis)
        drawPoint(node, axis)

        i = i + 1

    drawEdge(nodeList[0], nodeList[1])


#----- Calculate Drawing Settings -----#
# # !!! Demo without using Graph class
# # !!! A new layout algorithm should be implemented here !!!
# overlapNode1 = OverlapNode("ABCD_AEFGHI_AJKLMN_AQW_AYUIW")
# overlapNode2 = OverlapNode("DCBA_DOLK_DINXSV_DOPI_DYSU")

# # !!! This is only a brief demo. More generalized layout calculation should be implemented here !!!
# tempNode = overlapNode1.findSubNode("ABCD")
# # tempNodeCenter = [tempNode.getXAnchor(), tempNode.getYAnchor()]
# tempNodeEnd2 = tempNode.getEnd2Coordinate()
# overlapNode2.setxCenter(tempNodeEnd2[0])
# overlapNode2.setyCenter(tempNodeEnd2[1])
# tempNodeAngle = tempNode.getAngle()

# # !!! Demo using Graph class
# graphDemo = Graph()
# graphDemo.readInput("sample_input.txt")
# overlapNodeList = graphDemo.getNodeList()
# overlapNodeDemo1 = overlapNodeList[0]
# overlapNodeDemo2 = overlapNodeList[1]

# tempNode = overlapNodeDemo1.findSubNode("ABCD")
# tempNodeEnd2 = tempNode.getEnd2Coordinate()
# overlapNodeDemo2.setxCenter(tempNodeEnd2[0])
# overlapNodeDemo2.setyCenter(tempNodeEnd2[1])
# tempNodeAngle = tempNode.getAngle()

# # Need a LayoutAlgorithmOverlap.py !!!
# # Need to add edge connection into LayoutAlgorithmOverlap.py
# # Add draw edge into overlapDraw - FINISHED


# #----- Draw Overlapped Layout Graph -----#
# # Specify the size of figure window
# f,(ax1) = plt.subplots(1,1,figsize=(10,9))
# f.subplots_adjust(hspace=0,wspace=0)

# # Draw grpah
# # !!! Demo without using Graph class
# # drawPattern1(overlapNode1, 0)
# # drawPattern1(overlapNode2, tempNodeAngle - 180)
# # !!! Demo using Graph class
# drawPattern1(overlapNodeDemo1, 0, ax1)
# drawPattern1(overlapNodeDemo2, tempNodeAngle - 180, ax1)

# # Specify the axis settings
# plt.grid(True)
# ax1.set_xlim(-6,6)
# ax1.set_ylim(-6,6)

# #----- Draw Original Layout Graph -----#
# f,(ax2) = plt.subplots(1,1,figsize=(10,9))
# f.subplots_adjust(hspace=0,wspace=0)

# calLayout(graphDemo)
# overlapNodeList = graphDemo.getNodeList()
# overlapNodeDemo1 = overlapNodeList[0]
# overlapNodeDemo2 = overlapNodeList[1]

# drawPattern1(overlapNodeDemo1, 0, ax2)
# drawPattern1(overlapNodeDemo2, tempNodeAngle - 180, ax2)

# ax2.set_xlim(-6,6)
# ax2.set_ylim(-6,6)

# plt.show()