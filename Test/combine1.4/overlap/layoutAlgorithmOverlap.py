# -*- coding: UTF-8 -*-
from pyparsing import Or
from overlapNode import OverlapNode
from overlapGroup import OverlapGroup
import math
import numpy as np


# ----- Calculate node positions of a overlapNode for PATTERN 1 -----#
def calNodePosition(overlapNode, startAngle, situationNum):
    nodeList = overlapNode.getNodesContain()
    center = overlapNode.getCenter()
    nodeNum = overlapNode.getNodeNum()
    rotateRate = 360 / nodeNum

    i = 0
    for node in nodeList:
        literalsLengthHalf = node.getLiteralsLength() / 2
        rotateAngle = startAngle + rotateRate * i

        if situationNum == 2:
            if rotateAngle == 0 or rotateAngle == 180:
                rotateAngle -= 20

        node.setAngle(rotateAngle)
        nodeCenter = [center[0] + literalsLengthHalf * math.cos(math.radians(rotateAngle)),
                      center[1] + literalsLengthHalf * math.sin(math.radians(rotateAngle))]
        node.adjustX(nodeCenter[0])
        node.adjustY(nodeCenter[1])

        i = i + 1


# ----- Calculate node positions of a overlapNode for PATTERN 2 -----#
# radiusList[] -> Main difference from PATTERN 1!!! Maybe add another property in OverlapNode2 class
def calNodePosition2(overlapNode, startAngle, situationNum):
    overlapPart = overlapNode.getOverlapPart()
    remainNodeList = overlapNode.getRemainList()
    center = overlapNode.getCenter()
    nodeNum = len(remainNodeList)
    rotateRate = 360 / nodeNum

    overlapPart = overlapNode.getOverlapPart()
    overlapPart.adjustX(center[0])
    overlapPart.adjustY(center[1])

    i = 0
    startrRadius = 0.7
    radiusList = []  # Main difference from PATTERN 1!!! Maybe add another property in OverlapNode2 class

    for node in remainNodeList:
        radius = startrRadius + 0.15 * i
        rotateAngle = startAngle + rotateRate * i
        rectLength = node.getNodeWidth()

        if situationNum == 2:
            if rotateAngle == 0 or rotateAngle == 180:
                rotateAngle -= 20

        halfRecHeight = 0.25
        halfSectorAngle = np.arcsin(halfRecHeight / radius)
        calLength = radius * math.cos(halfSectorAngle) + rectLength / 2
        nodeCenter = [center[0] + calLength * math.cos(math.radians(rotateAngle)),
                      center[1] + calLength * math.sin(math.radians(rotateAngle))]
        node.adjustX(nodeCenter[0])
        node.adjustY(nodeCenter[1])
        node.setAngle(rotateAngle)

        radiusList.append(radius)
        i = i + 1

    overlapNode.setRadiusList(radiusList)


# ----- Calculate node positions of a overlapNode Pair for PATTERN 1 -----#
def calPairedPositions(overlapNodePair, initialCenter):
    overlapNode1 = overlapNodePair[0]
    overlapNode2 = overlapNodePair[1]
    pairNode = overlapNode1.getPairedNode()
    pairNodeName = pairNode.getName()

    overlapNode1.setxCenter(initialCenter[0])
    overlapNode1.setyCenter(initialCenter[1])

    calNodePosition(overlapNode1, 0, 1)

    pairNode = overlapNode1.findSubNode(pairNodeName)
    pairNodeEnd2 = pairNode.getEnd2Coordinate()

    overlapNode2.setxCenter(pairNodeEnd2[0])
    overlapNode2.setyCenter(pairNodeEnd2[1])

    angle2 = pairNode.getAngle()
    calNodePosition(overlapNode2, angle2 - 180, 1)


# ----- Calculate node positions of a overlapNode Pair for PATTERN 2 -----#
def calPairedPositions2(overlapNodePair, initialCenter):
    overlapNode1 = overlapNodePair[0]
    overlapNode2 = overlapNodePair[1]
    pairNode = overlapNode1.getPairedNode()
    pairNodeName = pairNode.getName()

    overlapPart1Name = overlapNode1.getOverlapPart().getName()
    overlapPart2Name = overlapNode2.getOverlapPart().getName()
    newPairNodeName = pairNodeName.strip(overlapPart1Name)
    newPairNodeName = newPairNodeName.strip(overlapPart2Name)

    tempStr1 = pairNodeName.strip(overlapPart1Name)
    tempStr2 = pairNodeName.strip(overlapPart2Name)[::-1]

    overlapNode1.findSubRemainNode(tempStr1).setName(newPairNodeName)

    overlapNode2.findSubRemainNode(tempStr2).setName(newPairNodeName[::-1])

    overlapNode1.setxCenter(initialCenter[0])
    overlapNode1.setyCenter(initialCenter[1])
    calNodePosition2(overlapNode1, 0, 1)

    pairNode = overlapNode1.findSubRemainNode(newPairNodeName)
    pairNodeWidth = pairNode.getNodeWidth()
    pairNodeHeight = pairNode.getNodeHeight()
    pairNodeAngle = pairNode.getAngle()

    # The default overlap is the inner layer
    currentRadius = 0.7
    centerDistance = math.sqrt(currentRadius * currentRadius - pairNodeHeight * pairNodeHeight / 4) * 2 + pairNodeWidth

    overlapNode1Center = overlapNode1.getCenter()
    overlapNode2.setxCenter(overlapNode1Center[0] + centerDistance * math.cos(math.radians(pairNodeAngle)))
    overlapNode2.setyCenter(overlapNode1Center[1] + centerDistance * math.sin(math.radians(pairNodeAngle)))

    angle2 = pairNode.getAngle()
    calNodePosition2(overlapNode2, angle2 - 180, 1)


# ----- Helper function to find the connection node in a overlapNode -----#
def findConnectionNode(overlapNode):
    for node in overlapNode.getNodesContain():
        if node.checkIsConnected() == True:
            return node


# ----- Calculate group positions of a group of overlapNode for PATTERN 1 -----#
def calGroupPosition1(overlapGroup, initialCenter):
    overlapNodeList = overlapGroup.getOverlapNodeList()

    if len(overlapNodeList) == 2:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))

        overlapNodePair = [overlapNode1, overlapNode2]
        calPairedPositions(overlapNodePair, initialCenter)
    else:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        overlapNode2.setPairedNode(findConnectionNode(overlapNode1))

        overlapNodePair = [overlapNode1, overlapNode2]
        calPairedPositions(overlapNodePair, initialCenter)

        overlapConnectNode1 = findConnectionNode(overlapNode1)

        connectionName = overlapConnectNode1.getName()
        center1 = overlapNode1.getCenter()
        angle1 = overlapConnectNode1.getAngle()

        for nextOverlapNode in overlapNodeList[2::]:
            nextOverlapConnectNode = findConnectionNode(nextOverlapNode)
            nextOverlapPartName = nextOverlapNode.getOverlapPartName()
            overlapPosition = connectionName.find(nextOverlapPartName)

            moveDistance = 0.18 * 4 * overlapPosition
            nextCenter = [center1[0] + moveDistance * math.cos(math.radians(angle1)),
                          center1[1] + moveDistance * math.sin(math.radians(angle1))]
            nextOverlapNode.setxCenter(nextCenter[0])
            nextOverlapNode.setyCenter(nextCenter[1])

            nextOverlapNode.removeNode(nextOverlapConnectNode.getName())

            remainNodeNum = len(nextOverlapNode.getNodesContain())
            startAngle = 360 / remainNodeNum + angle1

            calNodePosition(nextOverlapNode, startAngle + 60, 2)


# ----- Calculate group positions of a group of overlapNode for PATTERN 2 -----#
def calGroupPosition2(overlapGroup, initialCenter):
    overlapNodeList = overlapGroup.getOverlapNodeList()

    if len(overlapNodeList) == 2:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))

        overlapNodePair = [overlapNode1, overlapNode2]
        calPairedPositions2(overlapNodePair, initialCenter)
    else:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]
        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))

        overlapNodePair = [overlapNode1, overlapNode2]
        calPairedPositions2(overlapNodePair, initialCenter)

        overlapConnectNode1 = findConnectionNode(overlapNode1)

        connectionName = overlapConnectNode1.getName()
        center1 = overlapNode1.getCenter()
        angle1 = overlapConnectNode1.getAngle()

        for nextOverlapNode in overlapNodeList[2::]:
            nextOverlapConnectNode = findConnectionNode(nextOverlapNode)
            nextOverlapPart = nextOverlapNode.getOverlapPart()
            nextOverlapPartName = nextOverlapPart.getName()

            overlapPosition = connectionName.find(nextOverlapPartName[::-1])  # Possibly NEED refinement!!!

            nextOverlapNode.getOverlapPart().setName(
                nextOverlapNode.getOverlapPart().getName()[::-1])  # Possibly NEED refinement

            overlapNode1_OverlapPartNameLength = len(overlapNode1.getOverlapPart().getName())
            nextOverlapNode_OverlapPartLength_half = nextOverlapNode.getOverlapPart().getLiteralsLength() / 2
            moveDistance = math.sqrt(0.7 * 0.7 - 0.25 * 0.25) + 1 + 0.18 * 4 * (
                        overlapPosition - overlapNode1_OverlapPartNameLength) + nextOverlapNode_OverlapPartLength_half

            nextCenter = [center1[0] + moveDistance * math.cos(math.radians(angle1)),
                          center1[1] + moveDistance * math.sin(math.radians(angle1))]
            nextOverlapNode.setxCenter(nextCenter[0])
            nextOverlapNode.setyCenter(nextCenter[1])

            nextOverlapConnectNodeIndex = nextOverlapNode.getNodesContain().index(nextOverlapConnectNode)
            nextOverlapNode.removeNode(nextOverlapConnectNode.getName())

            remainNodeName = nextOverlapNode.getRemainList()[nextOverlapConnectNodeIndex].getName()
            nextOverlapNode.removeRemainNode(remainNodeName)

            remainNodeNum = len(nextOverlapNode.getNodesContain())
            startAngle = 360 / remainNodeNum + angle1

            calNodePosition2(nextOverlapNode, startAngle + 60, 2)


# ----- Cross product determination -----#
# def cross(p1,p2,p3):
#     x1=p2[0]-p1[0]
#     y1=p2[1]-p1[1]
#     x2=p3[0]-p1[0]
#     y2=p3[1]-p1[1]
#     return x1*y2-x2*y1

# ----- Detect whether two line segments cross each other -----#
# def segment(p1,p2,p3,p4):
#     if(max(p1[0],p2[0])>=min(p3[0],p4[0])
#     and max(p3[0],p4[0])>=min(p1[0],p2[0])
#     and max(p1[1],p2[1])>=min(p3[1],p4[1])
#     and max(p3[1],p4[1])>=min(p1[1],p2[1])):
#       if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0
#         and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
#         D=1
#       else:
#         D=0
#     else:
#       D=0
#     return D

# ----- Detect of an edge and a node are overlapped -----#
# def ifEdgeOverlap(l1,l2,sq):
#     # step 1 check if end point is in the square
#     if ( l1[0] >= sq[0] and l1[1] >= sq[1] and  l1[0] <= sq[2] and  l1[1] <= sq[3]) or ( l2[0] >= sq[0] and l2[1] >= sq[1] and  l2[0] <= sq[2] and  l2[1] <= sq[3]):
#         return 1
#     else:
#         # step 2 check if diagonal cross the segment
#         p1 = [sq[0],sq[1]]
#         p2 = [sq[2],sq[3]]
#         p3 = [sq[2],sq[1]]
#         p4 = [sq[0],sq[3]]
#         if segment(l1,l2,p1,p2) or segment(l1,l2,p3,p4):
#             return 1
#         else:
#             return 0

# ----- Detect if two rectangles are overlapped according to the postions of these two -----#
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


# ----- Check whether there is an intersection between two line segments -----#
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
        if ls1[0, 0] == ls2[0, 0] and (
                ls1_yRange[0] <= ls2[0, 1] <= ls1_yRange[1] or ls1_yRange[0] <= ls2[1, 1] <= ls1_yRange[1] or
                ls2_yRange[0] <= ls1[0, 1] <= ls2_yRange[1] or ls2_yRange[0] <= ls1[1, 1] <= ls2_yRange[1]):
            return True
        else:
            return False
    # If ls1 parallel to y-axis but ls2 not
    elif ls1[0, 0] == ls1[1, 0]:
        # ls2 = k2x + b2
        k2 = (ls2[1, 1] - ls2[0, 1]) / (ls2[1, 0] - ls2[0, 0])
        b2 = ls2[0, 1] - k2 * ls2[0, 0]

        y_intersect = k2 * ls1[0, 0] + b2

        if (ls1_yRange[0] <= y_intersect <= ls1_yRange[1] and ls2_yRange[0] <= y_intersect <= ls2_yRange[1]) and (
                ls1_xRange[0] <= ls1[0, 0] <= ls1_xRange[1] and ls2_xRange[0] <= ls1[0, 0] <= ls2_xRange[1]):
            return True
        else:
            return False
    # If ls2 parallel to y-axis but ls2 not
    elif ls2[0, 0] == ls2[1, 0]:
        # ls1 = k1x + b1
        k1 = (ls1[1, 1] - ls1[0, 1]) / (ls1[1, 0] - ls1[0, 0])
        b1 = ls1[0, 1] - k1 * ls1[0, 0]

        y_intersect = k1 * ls2[0, 0] + b1

        if (ls1_yRange[0] <= y_intersect <= ls1_yRange[1] and ls2_yRange[0] <= y_intersect <= ls2_yRange[1]) and (
                ls1_xRange[0] <= ls2[0, 0] <= ls1_xRange[1] and ls2_xRange[0] <= ls2[0, 0] <= ls2_xRange[1]):
            return True
        else:
            return False
    # If both ls1 and ls2 not parallel to the y-axis
    else:
        # ls1 = k1x + b1
        k1 = (ls1[1, 1] - ls1[0, 1]) / (ls1[1, 0] - ls1[0, 0])
        b1 = ls1[0, 1] - k1 * ls1[0, 0]
        # ls2 = k2x + b2
        k2 = (ls2[1, 1] - ls2[0, 1]) / (ls2[1, 0] - ls2[0, 0])
        b2 = ls2[0, 1] - k2 * ls2[0, 0]
        # if slopes are equal then parallel
        if k1 == k2:
            if b1 == b2:
                if (ls1_yRange[0] <= ls2[0, 1] <= ls1_yRange[1] or ls1_yRange[0] <= ls2[1, 1] <= ls1_yRange[1] or
                    ls2_yRange[0] <= ls1[0, 1] <= ls2_yRange[1] or ls2_yRange[0] <= ls1[1, 1] <= ls2_yRange[1]) and (
                        ls1_xRange[0] <= ls2[0, 0] <= ls1_xRange[1] or ls1_xRange[0] <= ls2[1, 0] <= ls1_xRange[1] or
                        ls2_xRange[0] <= ls1[0, 0] <= ls2_xRange[1] or ls2_xRange[0] <= ls1[1, 0] <= ls2_xRange[1]):
                    return True
                else:
                    return False
            else:
                return False
        else:
            x_intersect = (b2 - b1) / (k1 - k2)
            if ls1_xRange[0] <= x_intersect <= ls1_xRange[1] and ls2_xRange[0] <= x_intersect <= ls2_xRange[1]:
                return True

            return False


# ----- Calculate the edge connection positions of two nodes -----#
def calEdgePosition(node1, node2):
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

    return drawPointPair


# ----- Calculate the distance between two points -----#
def calDistance(point1, point2):
    # distance = math.sqrt((point1[0]-point2[0]) ^ 2 + (point1[1]-point2[1]) ^ 2)
    distance = math.sqrt(
        (point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]))
    return distance


# ----- Find a certain overlapNode from a list -----#
def findOverlapNode(overlapNodeList, name):
    for overlapNode in overlapNodeList:
        if name == overlapNode.getName():
            return overlapNode


# ----- Calculate the layout for a graph -----#
def calOverlapLayout(graph, patternNum):
    overallNodeList = graph.getNodeList()

    # -- Separate overlapped nodes and un-overlapped nodes --#
    overlapNodeList = []
    aloneNodeList = []
    for node in overallNodeList:
        if isinstance(node, OverlapNode):
            overlapNodeList.append(node)
        else:
            aloneNodeList.append(node)

    overlapGroupList = []

    # -- Seperate paired-overlapped nodes from overlapped nodes --#
    i = 0
    for overlapNode in overlapNodeList:
        nodeList = overlapNode.getNodesContain()

        if i < len(overlapNodeList) - 1:
            for node in nodeList:
                overlapNodeGroup = [overlapNode]  # !!!
                nodeName = node.getName()  # !!!

                for nextOverlapNode in overlapNodeList[i + 1:]:
                    if nextOverlapNode.checkIsPaired():
                        continue
                    nextNodeList = nextOverlapNode.getNodesContain()

                    for nextNode in nextNodeList:
                        if sorted(node.getName()) == sorted(nextNode.getName()):
                            overlapNode.setIsPaired(True)
                            nextOverlapNode.setIsPaired(True)
                            node.setIsConnected(True)
                            nextNode.setIsConnected(True)
                            if patternNum == 2:
                                thisConnectRemain = node.getName().lstrip(overlapNode.getOverlapPart().getName())
                                nextConnectRemain = nextNode.getName().lstrip(
                                    nextOverlapNode.getOverlapPart().getName())
                                # print([overlapNode.getOverlapPart().getName(), nextOverlapNode.getOverlapPart().getName()])
                                # print([thisConnectRemain, nextConnectRemain])
                                thisConnectRemainNode = overlapNode.findSubRemainNode(thisConnectRemain)
                                nextConnectRemainNode = nextOverlapNode.findSubRemainNode(nextConnectRemain)
                                thisConnectRemainNode.setIsConnected(True)
                                nextConnectRemainNode.setIsConnected(True)

                            overlapNodeGroup.append(nextOverlapNode)

                if len(overlapNodeGroup) != 1:
                    overlapGroupList.append(OverlapGroup(overlapNodeGroup, nodeName))

        i = i + 1

    # -- Seperate un-paired-overlapped nodes from overlapped nodes --#
    overlapUnpairList = []
    for overlapNode in overlapNodeList:
        if overlapNode.checkIsPaired() == False:
            overlapUnpairList.append(overlapNode)

    mapCenter = [0, 0]

    # -- Calculate the positions of grouped-overlapped nodes --#
    overlapGroupNum = len(overlapGroupList)

    count = overlapGroupNum / 2 - 0.5
    overlapPairHeightList = []

    if overlapGroupNum != 0:
        groupRadiusList = []
        for overlapGroup in overlapGroupList:
            overlapNode1Radius = overlapGroup.getOverlapNodeList()[0].getRadius()
            overlapNode2Radius = overlapGroup.getOverlapNodeList()[1].getRadius()
            overlapPairWidth = overlapNode1Radius + overlapNode2Radius
            groupRadiusList.append(overlapPairWidth)
        groupRadius = max(groupRadiusList) + 5

        i = 0
        rotateRate = 360 / overlapGroupNum
        for overlapGroup in overlapGroupList:
            overlapNode1Radius = overlapGroup.getOverlapNodeList()[0].getRadius()
            overlapNode2Radius = overlapGroup.getOverlapNodeList()[1].getRadius()
            overlapPairWidth = overlapNode1Radius + overlapNode2Radius

            overlapPairHeight = overlapNode1Radius + overlapNode2Radius
            overlapPairHeightList.append(overlapPairHeight)

            rotateAngle = rotateRate * i
            initialCenter = [mapCenter[0] - overlapPairWidth / 4, mapCenter[1] + overlapPairHeight * count]
            # initialCenter = [mapCenter[0] + groupRadius * math.cos(math.radians(rotateAngle)), mapCenter[1] + groupRadius * math.sin(math.radians(rotateAngle))]

            if overlapGroupNum == 1:
                initialCenter == [0, 0]

            if patternNum == 1:
                calGroupPosition1(overlapGroup, initialCenter)
            else:
                calGroupPosition2(overlapGroup, initialCenter)

            count = count - 1
            i += 1

        pairedRadius = sum(overlapPairHeightList) / 2 + 4
        # pairedRadius = groupRadius
    else:
        overlapPairWidth = 0
        pairedRadius = 0

    # -- Calculate the positions of un-paired-overlapped nodes --#
    overlapUnpairNum = len(overlapUnpairList)

    if overlapUnpairNum != 0:
        if sum(overlapPairHeightList) >= overlapPairWidth:
            pairedRadius = sum(overlapPairHeightList) / 2 + 4  # !!! Possibly NEED further calculation !!!
        else:
            pairedRadius = overlapPairWidth + 4  # !!! Possibly NEED further calculation !!!

        if pairedRadius == 0:
            pairedRadius = 5

        i = 0
        rotateRate = 360 / overlapUnpairNum
        overlapUnpairNodeLengthList = []

        for overlapUnpair in overlapUnpairList:
            rotateAngle = rotateRate * i
            center = [mapCenter[0] + pairedRadius * math.cos(math.radians(rotateAngle)),
                      pairedRadius * math.sin(math.radians(rotateAngle))]
            overlapUnpair.setxCenter(center[0])
            overlapUnpair.setyCenter(center[1])

            if patternNum == 1:
                calNodePosition(overlapUnpair, 0, 1)
            else:
                calNodePosition2(overlapUnpair, 0, 1)
            i = i + 1

            for node in overlapUnpair.getNodesContain():
                overlapUnpairNodeLengthList.append(node.getNodeWidth())
    else:
        overlapUnpairNodeLengthList = [0]

    # -- Calculate the positions of alone nodes --#
    aloneNodeNum = len(aloneNodeList)
    if aloneNodeNum != 0:
        # print(pairedRadius)
        overlappedRadius = pairedRadius + max(overlapUnpairNodeLengthList) + aloneNodeNum / 10 * 10 + 5
        # overlappedRadius = pairedRadius + max(overlapUnpairNodeLengthList) - 2
        # print(overlappedRadius)
        i = 0
        rotateRate = 360 / aloneNodeNum

        for node in aloneNodeList:
            rotateAngle = rotateRate * i
            center = [mapCenter[0] + overlappedRadius * math.cos(math.radians(rotateAngle)),
                      overlappedRadius * math.sin(math.radians(rotateAngle))]
            node.adjustX(center[0])
            node.adjustY(center[1])

            i = i + 1
    else:
        overlappedRadius = pairedRadius + max(overlapUnpairNodeLengthList) + 2

    # -- Use repulsive force to push away overlapped nodes --#
    # Put all nodes in a list - allNodeList
    allNodeList = []
    for overlapGroup in overlapGroupList:
        allOverlapNodeList = overlapGroup.getOverlapNodeList()
        for overlapNode in allOverlapNodeList:
            if patternNum == 1:
                allNode = overlapNode.getNodesContain()
                for node in allNode:
                    allNodeList.append(node)
            elif patternNum == 2:
                allNode = overlapNode.getRemainList()
                for node in allNode:
                    allNodeList.append(node)

    for overlapNode in overlapUnpairList:
        if patternNum == 1:
            allNode = overlapNode.getNodesContain()
        elif patternNum == 2:
            allNode = overlapNode.getRemainList()

        for node in allNode:
            allNodeList.append(node)

    for node in aloneNodeList:
        allNodeList.append(node)

    # print("Start checking overlap")
    # Check whether two nodes which shouldn't overlap are overlaped
    i = 0
    for node in allNodeList:
        for nextNode in allNodeList:
            # print([node.getName(), nextNode.getName()])
            if node.getName() == nextNode.getName():
                continue

            if node.getOverlapName() == nextNode.getOverlapName() and len(node.getOverlapName()) != 0:
                continue
            elif node.checkIsConnected() or nextNode.checkIsConnected():
                continue
            else:
                nodePos = node.getNodeCorners()
                nextNodePos = nextNode.getNodeCorners()
                isOverlap = ifOverlap(nodePos, nextNodePos)

                # -- Repulsive Force between nodes --#
                if isOverlap:
                    # print("Overlapped" + " " + node.getName() + " " + nextNode.getName())
                    # print([node.getXAnchor(), node.getYAnchor()])
                    # print(nodePos)
                    # print([nextNode.getXAnchor(), nextNode.getYAnchor()])
                    # print(nextNodePos)
                    # print('\n')

                    counter = 0
                    while (isOverlap):
                        if counter > 30:
                            break
                        nodeAngle = node.getAngle() + 10
                        nextNodeAngle = nextNode.getAngle() - 10

                        thisOverlapNode = findOverlapNode(overlapNodeList, node.getOverlapName())
                        nextOverlapNode = findOverlapNode(overlapNodeList, nextNode.getOverlapName())

                        if isinstance(thisOverlapNode, OverlapNode) and isinstance(nextOverlapNode, OverlapNode):
                            thisCenter = thisOverlapNode.getCenter()
                            nextCenter = nextOverlapNode.getCenter()

                            if patternNum == 1:
                                literalsLengthHalf = node.getLiteralsLength() / 2
                                node.setAngle(nodeAngle)
                                nodeCenter = [thisCenter[0] + literalsLengthHalf * math.cos(math.radians(nodeAngle)),
                                              thisCenter[1] + literalsLengthHalf * math.sin(math.radians(nodeAngle))]
                                nodeOriginalCenter = [node.getXAnchor(), node.getYAnchor()]
                                node.adjustX(nodeCenter[0] - nodeOriginalCenter[0])
                                node.adjustY(nodeCenter[1] - nodeOriginalCenter[1])

                                nextNode.setAngle(nextNodeAngle)
                                nextLiteralsLengthHalf = nextNode.getLiteralsLength() / 2
                                nextNode.setAngle(nextNodeAngle)
                                nextNodeCenter = [
                                    nextCenter[0] + nextLiteralsLengthHalf * math.cos(math.radians(nextNodeAngle)),
                                    nextCenter[1] + nextLiteralsLengthHalf * math.sin(math.radians(nextNodeAngle))]
                                nextNodeOriginalCenter = [nextNode.getXAnchor(), nextNode.getYAnchor()]
                                nextNode.adjustX(nextNodeCenter[0] - nextNodeOriginalCenter[0])
                                nextNode.adjustY(nextNodeCenter[1] - nextNodeOriginalCenter[1])
                            elif patternNum == 2:
                                node.setAngle(nodeAngle)
                                nodePosition = thisOverlapNode.getRemainList().index(node)
                                nodeRadius = thisOverlapNode.getRadiusList()[nodePosition]

                                rectLength = node.getNodeWidth()
                                halfRecHeight = 0.25
                                halfSectorAngle = np.arcsin(halfRecHeight / nodeRadius)
                                calLength = nodeRadius * math.cos(halfSectorAngle) + rectLength / 2
                                nodeCenter = [thisCenter[0] + calLength * math.cos(math.radians(nodeAngle)),
                                              thisCenter[1] + calLength * math.sin(math.radians(nodeAngle))]
                                nodeOriginalCenter = [node.getXAnchor(), node.getYAnchor()]
                                node.adjustX(nodeCenter[0] - nodeOriginalCenter[0])
                                node.adjustY(nodeCenter[1] - nodeOriginalCenter[1])
                                node.setAngle(nodeAngle)

                                nextNode.setAngle(nextNodeAngle)
                                nextNodePosition = nextOverlapNode.getRemainList().index(nextNode)
                                nextNodeRadius = nextOverlapNode.getRadiusList()[nextNodePosition]

                                nextRectLength = nextNode.getNodeWidth()
                                nextHalfRecHeight = 0.25
                                nextHalfSectorAngle = np.arcsin(nextHalfRecHeight / nextNodeRadius)
                                nextCalLength = nextNodeRadius * math.cos(nextHalfSectorAngle) + nextRectLength / 2
                                nextNodeCenter = [nextCenter[0] + nextCalLength * math.cos(math.radians(nextNodeAngle)),
                                                  nextCenter[1] + nextCalLength * math.sin(math.radians(nextNodeAngle))]
                                nextNodeOriginalCenter = [nextNode.getXAnchor(), nextNode.getYAnchor()]
                                nextNode.adjustX(nextNodeCenter[0] - nextNodeOriginalCenter[0])
                                nextNode.adjustY(nextNodeCenter[1] - nextNodeOriginalCenter[1])
                                nextNode.setAngle(nextNodeAngle)
                        elif (not isinstance(thisOverlapNode, OverlapNode)) and isinstance(nextOverlapNode,
                                                                                           OverlapNode):
                            if node.getXAnchor() >= nextNode.getXAnchor():
                                node.adjustX(0.2)
                            elif node.getXAnchor() < nextNode.getXAnchor():
                                node.adjustX(-0.2)

                            if node.getYAnchor() >= nextNode.getYAnchor():
                                node.adjustY(0.2)
                            elif node.getXAnchor() < nextNode.getYAnchor():
                                node.adjustY(-0.2)
                        elif isinstance(thisOverlapNode, OverlapNode) and not (
                        isinstance(nextOverlapNode, OverlapNode)):
                            if nextNode.getXAnchor() >= node.getXAnchor():
                                nextNode.adjustX(0.2)
                            elif nextNode.getXAnchor() < node.getXAnchor():
                                nextNode.adjustX(-0.2)

                            if nextNode.getYAnchor() >= node.getYAnchor():
                                nextNode.adjustY(0.2)
                            elif nextNode.getXAnchor() < node.getYAnchor():
                                nextNode.adjustY(-0.2)
                        elif not (isinstance(thisOverlapNode, OverlapNode)) and not (
                        isinstance(nextOverlapNode, OverlapNode)):
                            if node.getXAnchor() >= nextNode.getXAnchor():
                                node.adjustX(0.1)
                                nextNode.adjustX(-0.1)
                            elif node.getXAnchor() < nextNode.getXAnchor():
                                node.adjustX(-0.1)
                                nextNode.adjustX(0.1)

                            if node.getYAnchor() >= nextNode.getYAnchor():
                                node.adjustY(0.1)
                                nextNode.adjustY(-0.1)
                            elif node.getXAnchor() < nextNode.getYAnchor():
                                node.adjustY(-0.1)
                                nextNode.adjustY(0.1)

                        counter += 1
                        nodePos = node.getNodeCorners()
                        nextNodePos = nextNode.getNodeCorners()
                        isOverlap = ifOverlap(nodePos, nextNodePos)

        # print("---- Move on ---")
        i = i + 1

    # -- Use repulsive forces between edges and nodes --#
    # edgeNodeList = graph.getEdgeList()
    # edgeList = []
    # for edgeNode in edgeNodeList:
    #     nodeName1 = edgeNode[0]
    #     nodeName2 = edgeNode[1]
    #     node1 = allNodeList[0]
    #     node2 = allNodeList[1]
    #     for node in allNodeList:
    #         if node.getName() == nodeName1:
    #             node1 = node
    #     for node in allNodeList:
    #         if node.getName() == nodeName2:
    #             node2 = node

    #     pointPair = calEdgePosition(node1, node2)
    #     edgeList.append(pointPair)

    # overlapNodeNameList = []
    # overlapGroupNameList = []

    # for overlapNode in overlapUnpairList:
    #     overlapNodeNameList.append(overlapNode.getName())

    # for overlapNodeGroup in overlapGroupList:
    #     overlapNodeInGroupList = overlapGroup.getOverlapNodeList()
    #     overlapNodeInGroupNameList = []
    #     for overlapNodeInGroup in overlapNodeInGroupList:
    #         overlapNodeInGroupNameList.append(overlapNodeInGroup.getName())
    #     overlapGroupNameList.append(overlapNodeInGroupNameList)

    # for edge in edgeList:
    #     for node in allNodeList:
    #         if ifEdgeOverlap(edge[0], edge[1], node.getNodeCorners()):
    #             if node.getOverlapName() != "":
    #                 overlapName = node.getOverlapName()

    #                 for overlapNodeInGroupNameList in overlapGroupNameList:
    #                     for overlapNodeInGroup in overlapNodeInGroupNameList:
    #                         if overlapName == overlapNodeInGroup:
    #                             index = overlapGroupNameList.index(overlapNodeInGroupNameList)
    #                             overlapGroup = overlapGroupList[index]
    #                             for overlapNode in overlapGroup:
    #                                 overlapNode.adjustX(0.5)

    #                 for overlapNodeName in overlapNodeList:
    #                     if overlapName == overlapNodeNameList:
    #                         index = overlapNodeList.index(overlapNodeName)
    #                         overlapNode = overlapUnpairList[index]
    #                         overlapNode.adjustX(-0.5)
    #             else:
    #                 node.adjustX(0.2)

    # -- Calculate the map Radius --#
    aloneNodeLengthList = []
    for node in aloneNodeList:
        aloneNodeLengthList.append(node.getNodeWidth())
    if len(aloneNodeLengthList) != 0:
        mapRadius = overlappedRadius + max(aloneNodeLengthList)
    else:
        mapRadius = overlappedRadius

    return ([-mapRadius, mapRadius])