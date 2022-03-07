from tabnanny import check
import numpy as np
import math
from graph import Graph
from node import Node
from overlapNode import OverlapNode


# Detect if two rectangles are overlapped according to the postions of these two
# rectangles' four corners
# pos1 = pos2 = [[X1, Y1], [X2, Y2], [X3, Y3], [X4, Y4]]
# Left-Up, Left-Down, Right-Up, Right-Down
# Did not consider if one rectangle is in another rectangle
def ifOverlap(pos1, pos2):
    pos1_ls1 = [pos1[0], pos1[1]]
    pos1_ls2 = [pos1[0], pos1[2]]
    pos1_ls3 = [pos1[2], pos1[3]]
    pos1_ls4 = [pos1[1], pos1[3]]
    pos1_lss = [pos1_ls1, pos1_ls2, pos1_ls3, pos1_ls4]

    pos2_ls1 = [pos2[0], pos2[1]]
    pos2_ls2 = [pos2[0], pos2[2]]
    pos2_ls3 = [pos2[2], pos2[3]]
    pos2_ls4 = [pos2[1], pos2[3]]
    pos2_lss = [pos2_ls1, pos2_ls2, pos2_ls3, pos2_ls4]

    result = False

    for pos1_ls in pos1_lss:
        for pos2_ls in pos2_lss:
            result = result or ifIntersect(pos1_ls, pos2_ls)
            if result == True:
                break

    return result

# Check whether there is an intersection between two line segments
# ls stands for line segment, ls1 = ls2 = [[X1, Y1], [X2, Y2]]
# Helper function for ifOverlap


def ifIntersect(ls1, ls2):
    ls1 = np.array(ls1)
    ls2 = np.array(ls2)
    ls1_xRange = [ls1[0, 0], ls1[1, 0]] if ls1[0,
                                               0] < ls1[1, 0] else [ls1[1, 0], ls1[0, 0]]
    ls1_yRange = [ls1[0, 1], ls1[1, 1]] if ls1[0,
                                               1] < ls1[1, 1] else [ls1[1, 1], ls1[0, 1]]
    ls2_xRange = [ls2[0, 0], ls2[1, 0]] if ls2[0,
                                               0] < ls2[1, 0] else [ls2[1, 0], ls2[0, 0]]
    ls2_yRange = [ls2[0, 1], ls2[1, 1]] if ls2[0,
                                               1] < ls2[1, 1] else [ls2[1, 1], ls2[0, 1]]

    # If ls1 and ls2 parallel to y-axis
    if ls1[0, 0] == ls1[1, 0] and ls2[0, 0] == ls2[1, 0]:
        # If intersects
        if ls1[0, 0] == ls2[0, 0] and (ls1_yRange[0] <= ls2[0, 1] <= ls1_yRange[1] or ls1_yRange[0] <= ls2[1, 1] <= ls1_yRange[1] or ls2_yRange[0] <= ls1[0, 1] <= ls2_yRange[1] or ls2_yRange[0] <= ls1[1, 1] <= ls2_yRange[1]):
            return True
        else:
            return False
    # If ls1 parallel to y-axis but ls2 not
    elif ls1[0, 0] == ls1[1, 0]:
        # ls2 = k2x + b2
        k2 = (ls2[1, 1]-ls2[0, 1])/(ls2[1, 0]-ls2[0, 0])
        b2 = ls2[0, 1] - k2*ls2[0, 0]

        y_intersect = k2 * ls1[0, 0] + b2

        if (ls1_yRange[0] <= y_intersect <= ls1_yRange[1] or ls2_yRange[0] <= y_intersect <= ls2_yRange[1]):
            return True
        else:
            return False
    # If ls2 parallel to y-axis but ls2 not
    elif ls2[0, 0] == ls2[1, 0]:
        # ls1 = k1x + b1
        k1 = (ls1[1, 1]-ls1[0, 1])/(ls1[1, 0]-ls1[0, 0])
        b1 = ls1[0, 1] - k1*ls1[0, 0]

        y_intersect = k1 * ls2[0, 0] + b1

        if (ls1_yRange[0] <= y_intersect <= ls1_yRange[1] or ls2_yRange[0] <= y_intersect <= ls2_yRange[1]):
            return True
        else:
            return False
    # If both ls1 and ls2 not parallel to the y-axis
    else:
        # ls1 = k1x + b1
        k1 = (ls1[1, 1]-ls1[0, 1])/(ls1[1, 0]-ls1[0, 0])
        b1 = ls1[0, 1] - k1*ls1[0, 0]
        # ls2 = k2x + b2
        k2 = (ls2[1, 1]-ls2[0, 1])/(ls2[1, 0]-ls2[0, 0])
        b2 = ls2[0, 1] - k2*ls2[0, 0]
        # if slopes are equal then parallel
        if k1 == k2:
            if b1 == b2:
                if ls1_yRange[0] <= ls2[0, 1] <= ls1_yRange[1] or ls1_yRange[0] <= ls2[1, 1] <= ls1_yRange[1] or ls2_yRange[0] <= ls1[0, 1] <= ls2_yRange[1] or ls2_yRange[0] <= ls1[1, 1] <= ls2_yRange[1]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            x_intersect = (b2 - b1)/(k1-k2)
            if ls1_xRange[0] <= x_intersect <= ls1_xRange[1] or ls2_xRange[0] <= x_intersect <= ls2_xRange[1]:
                return True

            return False


def calLayout(graph: Graph):
    # Put all nodes on the plain uniformly first
    nodeNumber = graph.getNodeNumber()
    nodeList = graph.getNodeList()
    row = math.ceil(math.sqrt(nodeNumber))
    positions = np.linspace(-6, 6, row)

    x_index, y_index = 0, 0
    for node in graph.getNodeList():
        if x_index == row:
            x_index = 0
            y_index = y_index + 1

        node.adjustX(positions[x_index])
        node.adjustY(positions[y_index])
        x_index = x_index + 1

    # Then do the layout work
    for v_id in range(0, nodeNumber):
        for other_id in range(0, nodeNumber):
            if v_id == other_id:
                continue

        max_loop = 0
        overlap = checkNodeOverlap(nodeList[v_id], nodeList[other_id])
        while overlap:
            if nodeList[v_id].getXAnchor() >= nodeList[other_id].getXAnchor():
                nodeList[v_id].adjustX(0.1)
                nodeList[other_id].adjustX(-0.1)
            elif nodeList[v_id].getXAnchor() < nodeList[other_id].getXAnchor():
                nodeList[other_id].adjustX(0.1)
                nodeList[v_id].adjustX(-0.1)

            if nodeList[v_id].getYAnchor() >= nodeList[other_id].getYAnchor():
                nodeList[v_id].adjustY(0.1)
                nodeList[other_id].adjustY(-0.1)
            elif nodeList[v_id].getYAnchor() < nodeList[other_id].getYAnchor():
                nodeList[other_id].adjustY(0.1)
                nodeList[v_id].adjustY(-0.1)

            max_loop = max_loop+1
            if max_loop >= 100:
                break


# Check if two nodes are overlapped (take OverlapNode class into consideration)
def checkNodeOverlap(node1, node2):
    if isinstance(node1, Node) and isinstance(node2, Node):
        return ifOverlap(node1.getCornersPos(), node2.getCornersPos())
    elif isinstance(node1, OverlapNode) and isinstance(node2, OverlapNode):
        result = False
        for node1_subnode in node1.getNodesContain():
            for node2_subnode in node2.getNodesContain():
                result = result and ifOverlap(node1_subnode, node2_subnode)

        return result
    else:
        result = False

        if isinstance(node2, OverlapNode):
            node1, node2 = node2, node1

        for node1_subnode in node1.getNodesContain():
            result = result and ifOverlap(node1_subnode, node2)

        return result


# TEMPORARY CODE #
a = Graph()
a.readInput("sample_input.txt")
calLayout(a)
print('a')
