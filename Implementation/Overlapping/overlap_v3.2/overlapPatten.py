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

from overlapDraw import drawEdge, drawLiteral
from overlapDraw import drawPoint
from overlapDraw import drawRectangle
from layoutAlgorithmOverlap import calOverlapLayout

def pattern1Draw(graph, axis):
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

    for overlapNode in overlapNodeList:
        nodeList = overlapNode.getNodesContain()
        for node in nodeList:
            drawLiteral(node)
            drawRectangle(node, axis)
            drawPoint(node, axis)
            allNodeList.append(node)

    for node in aloneNodeList:
        drawLiteral(node)
        drawRectangle(node, axis)
        drawPoint(node, axis)
        allNodeList.append(node)

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


graphDemo = Graph()
graphDemo.readInput("sample_input.txt")
calOverlapLayout(graphDemo)

#----- Draw Overlapped Layout Graph -----#
# Specify the size of figure window
f,(ax1) = plt.subplots(1,1,figsize=(10,9))
f.subplots_adjust(hspace=0,wspace=0)

pattern1Draw(graphDemo, ax1)

plt.grid(False)
ax1.set_xlim(-20,20)
ax1.set_ylim(-20,20)

plt.show()