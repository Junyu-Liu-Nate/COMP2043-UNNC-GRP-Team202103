#-- Overlap Pattern --#
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

from overlapDraw import drawArcCombo, drawEdge, drawLiteral
from overlapDraw import drawPoint
from overlapDraw import drawRectangle
from layoutAlgorithmOverlap import calOverlapLayout

#----- Draw pattern 1 -----#
def pattern1Draw(graph, axis, zoomRatio):
    overallNodeList = graph.getNodeList()
    edgeList = graph.getEdgeList()

    allNodeList = []

    # Separate overlapped nodes and un-overlapped nodes
    overlapNodeList = []
    aloneNodeList = []
    for node in overallNodeList:
        if isinstance(node, OverlapNode):
            overlapNodeList.append(node)
        else:
            aloneNodeList.append(node)

    # Draw nodes from overlapped Nodes and add nodes into allNodeList
    for overlapNode in overlapNodeList:
        nodeList = overlapNode.getNodesContain()
        for node in nodeList:
            drawLiteral(node, zoomRatio)
            drawRectangle(node, axis)
            drawPoint(node, axis)
            allNodeList.append(node)

    # Draw alone nodes and add nodes into allNodeList
    for node in aloneNodeList:
        drawLiteral(node, zoomRatio)
        drawRectangle(node, axis)
        drawPoint(node, axis)
        allNodeList.append(node)

    # Draw edges according to allNodeList
    for edge in edgeList:
        nodeName1 = edge[0]
        nodeName2 = edge[1]
        node1 = allNodeList[0]
        node2 = allNodeList[1]
        for node in allNodeList:
            if node.getName() == nodeName1:
                node1 = node
        for node in allNodeList:
            if node.getName() == nodeName2:
                node2 = node
        drawEdge(node1, node2)

#----- Draw Pattern 2 -----#
def pattern2Draw(graph, axis, zoomRatio):
    overallNodeList = graph.getNodeList()
    edgeList = graph.getEdgeList()

    allNodeNameList = []

    # Separate overlapped nodes and un-overlapped nodes
    overlapNodeList = []
    aloneNodeList = []
    for node in overallNodeList:
        if isinstance(node, OverlapNode):
            overlapNodeList.append(node)
        else:
            aloneNodeList.append(node)

    # Draw nodes from overlapped Nodes and add [nodes, full name] into allNodeNameList
    for overlapNode in overlapNodeList:
        remainNodeList = overlapNode.getRemainList()
        overlapPart = overlapNode.getOverlapPart()
        radiusList = overlapNode.getRadiusList()
        # rotateAngleList = overlapNode.getRotateAngleList()
        overlapNodeCenter = overlapNode.getCenter()

        i = 0
        for node in remainNodeList:
            drawArcCombo(overlapNodeCenter, radiusList[i], node.getAngle(), node, axis, zoomRatio)
            drawPoint(node, axis)
            allNodeNameList.append([node, overlapPart.getName() + node.getName()]) # muti-overlapped situation is overlooked!
            i = i + 1
        drawLiteral(overlapPart, zoomRatio)
    
    # Draw alone nodes and add [nodes, full name] into allNodeNameList
    for node in aloneNodeList:
        drawLiteral(node, zoomRatio)
        drawRectangle(node, axis)
        drawPoint(node, axis)
        allNodeNameList.append([node, node.getName()])

    # Draw edges according to allNodeNameList
    for edge in edgeList:
        nodeName1 = edge[0]
        nodeName2 = edge[1]
        node1 = allNodeNameList[0][0]   
        node2 = allNodeNameList[1][0]
        i = 0
        for nodeName in allNodeNameList:
            if nodeName[1] == nodeName1:
                node1 = nodeName[0]
            if nodeName[1] == nodeName2:
                node2 = nodeName[0]
        drawEdge(node1, node2)

#----- Read input file and calculate layout -----#
patternNum = input("Please enter the pattern number: ")

graphDemo = Graph()
graphDemo.readInput("debug1.txt", patternNum) # 2 represents pattern 2, NEED aumatic checking!!!
windowRange = calOverlapLayout(graphDemo, patternNum) # window range specifies the coordinate settings
# zoomRatio = x_max / 6
zoomRatio = windowRange[1] / 6
if zoomRatio == 0:
    zoomRatio = 1

#----- Draw Overlapped Layout Graph -----#
# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,9))
f.subplots_adjust(hspace=0,wspace=0)

if patternNum == 1:
    pattern1Draw(graphDemo, ax1, zoomRatio)
else:
    pattern2Draw(graphDemo, ax1, zoomRatio)
#pattern2Draw(graphDemo, ax1) # 2 represents pattern 2, NEED aumatic checking!!!

plt.grid(False)
# ax1.set_xlim(-6,6)
# ax1.set_ylim(-6,6)
ax1.set_xlim(windowRange[0],windowRange[1])
ax1.set_ylim(windowRange[0],windowRange[1])

# plt.savefig('results/test2.jpg')
plt.show()