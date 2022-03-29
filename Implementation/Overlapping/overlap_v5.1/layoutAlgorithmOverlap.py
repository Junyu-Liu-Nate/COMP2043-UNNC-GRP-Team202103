from pyparsing import Or
from overlapNode import OverlapNode
from overlapGroup import OverlapGroup
import math
import numpy as np

#----- Calculate node positions of a overlapNode for PATTERN 1 -----#
def calNodePosition(overlapNode, startAngle):
    nodeList = overlapNode.getNodesContain()
    center = overlapNode.getCenter()
    nodeNum = overlapNode.getNodeNum()
    rotateRate = 360 / nodeNum
    
    i = 0
    for node in nodeList:
        literalsLengthHalf = node.getLiteralsLength() / 2
        rotateAngle = startAngle + rotateRate * i
        node.setAngle(rotateAngle)
        nodeCenter = [center[0] + literalsLengthHalf * math.cos(math.radians(rotateAngle)), center[1] + literalsLengthHalf * math.sin(math.radians(rotateAngle))]
        node.adjustX(nodeCenter[0])
        node.adjustY(nodeCenter[1])

        i = i + 1

#----- Calculate node positions of a overlapNode for PATTERN 2 -----#
# radiusList[] -> Main difference from PATTERN 1!!! Maybe add another property in OverlapNode2 class
def calNodePosition2(overlapNode, startAngle):
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
    radiusList = [] # Main difference from PATTERN 1!!! Maybe add another property in OverlapNode2 class
    #rotateAngleList = []
    for node in remainNodeList:
        radius = startrRadius + 0.15 * i
        rotateAngle = startAngle + rotateRate * i
        rectLength = node.getNodeWidth()
    
        halfRecHeight = 0.25
        halfSectorAngle = np.arcsin(halfRecHeight / radius)
        calLength = radius * math.cos(halfSectorAngle) + rectLength / 2
        nodeCenter = [center[0] + calLength * math.cos(math.radians(rotateAngle)), center[1] + calLength * math.sin(math.radians(rotateAngle))]
        node.adjustX(nodeCenter[0])
        node.adjustY(nodeCenter[1])
        node.setAngle(rotateAngle)
        
        radiusList.append(radius)
        #rotateAngleList.append(startAngle + rotateRate * i)
        i = i + 1
    
    overlapNode.setRadiusList(radiusList)
    #overlapNode.setRotateAngleList(rotateAngleList)    

#----- Calculate node positions of a overlapNode Pair for PATTERN 1 -----#
def calPairedPositions(overlapNodePair, initialCenter):
    overlapNode1 = overlapNodePair[0]
    overlapNode2 = overlapNodePair[1]
    pairNode = overlapNode1.getPairedNode()
    pairNodeName = pairNode.getName()
    #print(pairNodeName)

    overlapNode1.setxCenter(initialCenter[0])
    overlapNode1.setyCenter(initialCenter[1])
    #print(overlapNode1.getCenter())
    calNodePosition(overlapNode1, 0)

    pairNode = overlapNode1.findSubNode(pairNodeName)
    pairNodeEnd2 = pairNode.getEnd2Coordinate()
    #print(pairNodeEnd2)
    overlapNode2.setxCenter(pairNodeEnd2[0])
    overlapNode2.setyCenter(pairNodeEnd2[1])
    #print(overlapNode2.getCenter())
    angle2 = pairNode.getAngle()
    calNodePosition(overlapNode2, angle2 - 180)

#----- Calculate node positions of a overlapNode Pair for PATTERN 2 -----#
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
    calNodePosition2(overlapNode1, 0)

    pairNode = overlapNode1.findSubRemainNode(newPairNodeName)
    pairNodeWidth = pairNode.getNodeWidth()
    pairNodeHeight = pairNode.getNodeHeight()
    pairNodeAngle = pairNode.getAngle() 

    # !!! This is just a demonstration of the 1st layer (inner most circle) !!!
    # !!! The default should be the inner most circle
    currentRadius = 0.7
    centerDistance = math.sqrt(currentRadius * currentRadius - pairNodeHeight * pairNodeHeight / 4) * 2 + pairNodeWidth

    overlapNode1Center = overlapNode1.getCenter()
    overlapNode2.setxCenter(overlapNode1Center[0] + centerDistance * math.cos(math.radians(pairNodeAngle)))
    overlapNode2.setyCenter(overlapNode1Center[1] + centerDistance * math.sin(math.radians(pairNodeAngle)))

    angle2 = pairNode.getAngle()
    calNodePosition2(overlapNode2, angle2 - 180)

#----- Helper function to find the connection node in a overlapNode -----#
def findConnectionNode(overlapNode):
    for node in overlapNode.getNodesContain():
        if node.checkIsConnected() == True:
            return node

#----- Calculate group positions of a group of overlapNode for PATTERN 1 -----#
def calGroupPosition1(overlapGroup, initialCenter):
    overlapNodeList = overlapGroup.getOverlapNodeList()
    # print("There are " + str(len(overlapNodeList)) + " in this overlapGroup")
    overlapNodeName = overlapGroup.getOverlapNodeName()

    if len(overlapNodeList) == 2:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        #print(findConnectionNode(overlapNode1).getName())
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))
        #print(findConnectionNode(overlapNode2).getName())
        #print(overlapNode1.getPairedNode().getName())
        #print(overlapNode2.getPairedNode().getName())

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
            nextCenter = [center1[0] + moveDistance * math.cos(math.radians(angle1)), center1[1] + moveDistance * math.sin(math.radians(angle1))]
            nextOverlapNode.setxCenter(nextCenter[0])
            nextOverlapNode.setyCenter(nextCenter[1])

            nextOverlapNode.removeNode(nextOverlapConnectNode.getName())

            remainNodeNum = len(nextOverlapNode.getNodesContain())
            startAngle = 360 / remainNodeNum + angle1

            calNodePosition(nextOverlapNode, startAngle + 60)

#----- Calculate group positions of a group of overlapNode for PATTERN 2 -----#
def calGroupPosition2(overlapGroup, initialCenter):
    overlapNodeList = overlapGroup.getOverlapNodeList()
    # print("There are " + str(len(overlapNodeList)) + " in this overlapGroup")
    overlapNodeName = overlapGroup.getOverlapNodeName()

    if len(overlapNodeList) == 2:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        #print(findConnectionNode(overlapNode1).getName())
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))
        #print(findConnectionNode(overlapNode2).getName())
        #print(overlapNode1.getPairedNode().getName())
        #print(overlapNode2.getPairedNode().getName())

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
        overlapPart1 = overlapNode1.getOverlapPart()
        overlapPart2 = overlapNode2.getOverlapPart()
        center1 = overlapNode1.getCenter()
        angle1 = overlapConnectNode1.getAngle()

        for nextOverlapNode in overlapNodeList[2::]:
            nextOverlapConnectNode = findConnectionNode(nextOverlapNode)
            #nextOverlapPartName = nextOverlapNode.getOverlapPartName()
            nextOverlapPart = nextOverlapNode.getOverlapPart()
            nextOverlapPartName = nextOverlapPart.getName()
            #print(nextOverlapPartName)
            #print(connectionName)
            overlapPosition = connectionName.find(nextOverlapPartName[::-1]) # NEED refinement!!!
            # print("Overlap position is " + str(overlapPosition))

            nextOverlapNode.getOverlapPart().setName(nextOverlapNode.getOverlapPart().getName()[::-1]) # NEED refinement
            #print("overlap position is " + str(overlapPosition))

            # connectionName1 = connectionName[0:overlapPosition - 1].strip(overlapPart1.getName())
            # connectionName2 = connectionName[overlapPosition:].strip(overlapPart2.getName())

            # overlapNode1.getRemainList()[0].setName(connectionName1)
            # overlapNode2.getRemainList()[1].setName(connectionName2)

            # !!!!!!!!!!--- BIG PROBLEM ---!!!!!!!!!!!
            overlapPartLength = len(nextOverlapPartName)
            overlapNode1_OverlapPartNameLength = len(overlapNode1.getOverlapPart().getName())
            nextOverlapNode_OverlapPartLength_half = nextOverlapNode.getOverlapPart().getLiteralsLength() / 2
            # moveDistance = 0.6 + 0.18 * 4 * overlapPosition # NEED refinement!!!
            moveDistance = math.sqrt(0.7 * 0.7 - 0.25 * 0.25) + 1 + 0.18 * 3 * (overlapPosition - overlapNode1_OverlapPartNameLength) + nextOverlapNode_OverlapPartLength_half

            #print("move distance is " + str(moveDistance))
            nextCenter = [center1[0] + moveDistance * math.cos(math.radians(angle1)), center1[1] + moveDistance * math.sin(math.radians(angle1))]
            nextOverlapNode.setxCenter(nextCenter[0])
            nextOverlapNode.setyCenter(nextCenter[1])

            nextOverlapConnectNodeIndex = nextOverlapNode.getNodesContain().index(nextOverlapConnectNode)
            nextOverlapNode.removeNode(nextOverlapConnectNode.getName())
            
            remainNodeName = nextOverlapNode.getRemainList()[nextOverlapConnectNodeIndex].getName()
            nextOverlapNode.removeRemainNode(remainNodeName)

            remainNodeNum = len(nextOverlapNode.getNodesContain())
            startAngle = 360 / remainNodeNum + angle1

            calNodePosition2(nextOverlapNode, startAngle + 60)

#--- Detect if two rectangles are overlapped according to the postions of these two ---#
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

#--- Check whether there is an intersection between two line segments ---#
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
            if ls1_xRange[0] <= x_intersect <= ls1_xRange[1] and ls2_xRange[0] <= x_intersect <= ls2_xRange[1]:
                return True

            return False


#----- Calculate the layout for a graph -----#
def calOverlapLayout(graph, patternNum):
    overallNodeList = graph.getNodeList()

    # Separate overlapped nodes and un-overlapped nodes
    overlapNodeList = []
    aloneNodeList = []
    for node in overallNodeList:
        if isinstance(node, OverlapNode):
            overlapNodeList.append(node)
        else:
            aloneNodeList.append(node)

    overlapGroupList = []

    # Seperate paired-overlapped nodes from overlapped nodes
    #overlapPairList = []
    connectNodeNameList = [] # used for prevent repeat
    jump = 0
    i = 0
    for overlapNode in overlapNodeList:
        jump = 0
        nodeList = overlapNode.getNodesContain()

        if i < len(overlapNodeList) - 1:
            for node in nodeList:
                overlapNodeGroup = [overlapNode] #!!!
                nodeName = node.getName() # !!!

                # if (len(connectNodeNameList) != 0):
                #     for name in connectNodeNameList:
                #         if sorted(name) == sorted(nodeName):
                #             jump = 1
                
                # if jump == 1:
                #     continue

                for nextOverlapNode in overlapNodeList[i + 1:]:
                    if nextOverlapNode.checkIsPaired():
                        continue
                    nextNodeList = nextOverlapNode.getNodesContain()
                    
                    for nextNode in nextNodeList:
                        # if node.getName() == nextNode.getName()[::-1]:
                        #     overlapNode.setIsPaired(True)
                        #     overlapNode.setPairedNode(node)
                        #     nextOverlapNode.setIsPaired(True)
                        #     nextOverlapNode.setPairedNode(node)
                            #overlapPairList.append([overlapNode, nextOverlapNode])
                        # !!!
                        # !!!!!!--- The problem of re-order ---!!!!!!
                        if sorted(node.getName()) == sorted(nextNode.getName()):
                            overlapNode.setIsPaired(True)
                            nextOverlapNode.setIsPaired(True)
                            node.setIsConnected(True)
                            nextNode.setIsConnected(True)

                            overlapNodeGroup.append(nextOverlapNode)
                            #print([sorted(node.getName()), sorted(nextNode.getName())])

                if len(overlapNodeGroup) != 1:
                    overlapGroupList.append(OverlapGroup(overlapNodeGroup, nodeName))

        i = i + 1

    # Seperate un-paired-overlapped nodes from overlapped nodes
    overlapUnpairList = []
    for overlapNode in overlapNodeList:
        if overlapNode.checkIsPaired() == False:
            overlapUnpairList.append(overlapNode)

    mapCenter = [0,0]

    # Calculate the positions of paired-overlapped nodes
    #overlapPairNum = len(overlapPairList)
    overlapGroupNum = len(overlapGroupList)
    #print("overlapGroup number is " + str(overlapGroupNum))
    count = overlapGroupNum / 2 - 0.5
    overlapPairHeightList = []

    # for overlapPair in overlapPairList:
    #     overlapNode1Radius = overlapPair[0].getRadius()
    #     overlapNode2Radius = overlapPair[1].getRadius()
    #     overlapPairWidth = overlapNode1Radius + overlapNode2Radius
    #     # overlapPairHeight = max([overlapNode1Radius, overlapNode2Radius])
    #     overlapPairHeight = overlapNode1Radius + overlapNode2Radius
    #     overlapPairHeightList.append(overlapPairHeight)

    #     initialCenter = [mapCenter[0] - overlapPairWidth / 4, mapCenter[1] + overlapPairHeight * count]
    #     #initialCenter = [0,0]

    #     if patternNum == 1:
    #         calPairedPositions(overlapPair, initialCenter)
    #     else:
    #         calPairedPositions2(overlapPair, initialCenter)
        
    #     count = count - 1

    if overlapGroupNum != 0:
        for overlapGroup in overlapGroupList:
            overlapNode1Radius = overlapGroup.getOverlapNodeList()[0].getRadius()
            overlapNode2Radius = overlapGroup.getOverlapNodeList()[1].getRadius()
            overlapPairWidth = overlapNode1Radius + overlapNode2Radius

            overlapPairHeight = overlapNode1Radius + overlapNode2Radius
            overlapPairHeightList.append(overlapPairHeight)

            initialCenter = [mapCenter[0] - overlapPairWidth / 4, mapCenter[1] + overlapPairHeight * count]
            #initialCenter = [0 - overlapPairWidth / 4, 0 + overlapPairHeight * count]
            #print(initialCenter)
            #initialCenter = [0,0]

            if patternNum == 1:
                # calPairedPositions(overlapGroup, initialCenter)
                calGroupPosition1(overlapGroup, initialCenter)
            else:
                #calPairedPositions2(overlapGroup, initialCenter)
                calGroupPosition2(overlapGroup, initialCenter)
        
            count = count - 1

        pairedRadius =  sum(overlapPairHeightList) / 2 + 4
    else:
        overlapPairWidth = 0
        pairedRadius = 0

    # Calculate the positions of un-paired-overlapped nodes
    overlapUnpairNum = len(overlapUnpairList)
    #print(overlapUnpairNum)

    if overlapUnpairNum != 0:
        if sum(overlapPairHeightList) >= overlapPairWidth:
            pairedRadius = sum(overlapPairHeightList) / 2 + 4 # !!! NEED further calculation !!!
        else:
            pairedRadius = overlapPairWidth + 4 # !!! NEED further calculation !!!

        if pairedRadius == 0:
            pairedRadius = 5

        i = 0
        rotateRate = 360 / overlapUnpairNum
        overlapUnpairNodeLengthList = []

        for overlapUnpair in overlapUnpairList:
            rotateAngle = rotateRate * i
            center = [mapCenter[0] + pairedRadius * math.cos(math.radians(rotateAngle)), pairedRadius * math.sin(math.radians(rotateAngle))]
            overlapUnpair.setxCenter(center[0])
            overlapUnpair.setyCenter(center[1])

            if patternNum == 1:
                calNodePosition(overlapUnpair, 0)
            else:
                calNodePosition2(overlapUnpair, 0)
            i = i + 1

            for node in overlapUnpair.getNodesContain():
                overlapUnpairNodeLengthList.append(node.getNodeWidth())
    else:
        overlapUnpairNodeLengthList = [0]

    # Calculate the positions of alone nodes
    aloneNodeNum = len(aloneNodeList)
    #print(aloneNodeNum)
    if aloneNodeNum != 0:
        #print(pairedRadius)
        overlappedRadius = pairedRadius + max(overlapUnpairNodeLengthList) + 4
        #print(overlappedRadius)
        i = 0
        rotateRate = 360 / aloneNodeNum

        for node in aloneNodeList:
            rotateAngle = rotateRate * i
            center = [mapCenter[0] + overlappedRadius * math.cos(math.radians(rotateAngle)), overlappedRadius * math.sin(math.radians(rotateAngle))]
            node.adjustX(center[0])
            node.adjustY(center[1])

            i = i + 1
    else:
        overlappedRadius = pairedRadius

    #--- Use repulsive force to push away overlapped nodes ---#
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

    # Check whether two nodes which shouldn't overlap are overlaped
    i = 0
    for node in allNodeList:
        print(node.getName())
        for nextNode in allNodeList[i + 1:]:
            if (node.getOverlapName() == nextNode.getOverlapName()):
                # print(node.getOverlapName())
                continue
            elif node.checkIsConnected() or nextNode.checkIsConnected():
                continue
            else:
                nodePos = node.getNodeCorners()
                nextNodePos = nextNode.getNodeCorners()
                #print((nodePos, nextNodePos))
                isOverlap = ifOverlap(nodePos, nextNodePos)

                if isOverlap:
                    print("Overlapped" + " " + node.getName() + " " + nextNode.getName())
                    print([node.getXAnchor(), node.getYAnchor()])
                    print(nodePos)
                    print([nextNode.getXAnchor(), nextNode.getYAnchor()])
                    print(nextNodePos)
                    print('\n')
                    nodeAngle = node.getAngle() - 10
                    nextNodeAngle = nextNode.getAngle() + 10

                    thisOverlapNode = findOverlapNode(overlapNodeList, node.getOverlapName())
                    nextOverlapNode = findOverlapNode(overlapNodeList, nextNode.getOverlapName())
                    if isinstance(thisOverlapNode, OverlapNode) and isinstance(nextOverlapNode, OverlapNode):
                        thisCenter = thisOverlapNode.getCenter()
                        nextCenter = nextOverlapNode.getCenter()

                        if patternNum == 1:
                            literalsLengthHalf = node.getLiteralsLength() / 2
                            #node.setAngle(nodeAngle)
                            nodeCenter = [thisCenter[0] + literalsLengthHalf * math.cos(math.radians(nodeAngle)), thisCenter[1] + literalsLengthHalf * math.sin(math.radians(nodeAngle))]
                            nodeOriginalCenter = [node.getXAnchor(), node.getYAnchor()]
                            #node.adjustX(nodeCenter[0] - nodeOriginalCenter[0])
                            #node.adjustY(nodeCenter[1] - nodeOriginalCenter[1])

                            #nextNode.setAngle(nextNodeAngle)
                            nextLiteralsLengthHalf = nextNode.getLiteralsLength() / 2
                            #nextNode.setAngle(nextNodeAngle)
                            nextNodeCenter = [nextCenter[0] + nextLiteralsLengthHalf * math.cos(math.radians(nextNodeAngle)), nextCenter[1] + nextLiteralsLengthHalf * math.sin(math.radians(nextNodeAngle))]
                            nextNodeOriginalCenter = [nextNode.getXAnchor(), nextNode.getYAnchor()]
                            #nextNode.adjustX(nextNodeCenter[0] - nextNodeOriginalCenter[0])
                            #nextNode.adjustY(nextNodeCenter[1] - nextNodeOriginalCenter[1])
                        elif patternNum == 2:
                            node.setAngle(nodeAngle)
                            nodePosition = thisOverlapNode.getRemainList().index(node)
                            nodeRadius = thisOverlapNode.getRadiusList()[nodePosition]

                            rectLength = node.getNodeWidth()
                            halfRecHeight = 0.25
                            halfSectorAngle = np.arcsin(halfRecHeight / nodeRadius)
                            calLength = nodeRadius * math.cos(halfSectorAngle) + rectLength / 2
                            nodeCenter = [thisCenter[0] + calLength * math.cos(math.radians(nodeAngle)), thisCenter[1] + calLength * math.sin(math.radians(nodeAngle))]
                            nodeOriginalCenter = [node.getXAnchor(), node.getYAnchor()]
                            #node.adjustX(nodeCenter[0] - nodeOriginalCenter[0])
                            #node.adjustY(nodeCenter[1] - nodeOriginalCenter[1])
                            #node.setAngle(nodeAngle)

                            nextNode.setAngle(nextNodeAngle)
                            nextNodePosition = nextOverlapNode.getRemainList().index(nextNode)
                            nextNodeRadius = nextOverlapNode.getRadiusList()[nextNodePosition]

                            nextRectLength = nextNode.getNodeWidth()
                            nextHalfRecHeight = 0.25
                            nextHalfSectorAngle = np.arcsin(nextHalfRecHeight / nextNodeRadius)
                            nextCalLength = nextNodeRadius * math.cos(nextHalfSectorAngle) + nextRectLength / 2
                            nextNodeCenter = [nextCenter[0] + nextCalLength * math.cos(math.radians(nextNodeAngle)), nextCenter[1] + nextCalLength * math.sin(math.radians(nextNodeAngle))]
                            nextNodeOriginalCenter = [nextNode.getXAnchor(), nextNode.getYAnchor()]
                            #nextNode.adjustX(nextNodeCenter[0] - nextNodeOriginalCenter[0])
                            #nextNode.adjustY(nextNodeCenter[1] - nextNodeOriginalCenter[1])
                            #nextNode.setAngle(nextNodeAngle)
                            # !!!!!!!!!!!!!!!!!!!!!!!!! 
                    elif (not isinstance(thisOverlapNode, OverlapNode)) and isinstance(nextOverlapNode, OverlapNode):
                        if node.getXAnchor() >= nextNode.getXAnchor():
                            node.adjustX(0.2)
                        elif node.getXAnchor() < nextNode.getXAnchor():
                            node.adjustX(-0.2)

                        if node.getYAnchor() >= nextNode.getYAnchor():
                            node.adjustY(0.2)
                        elif node.getXAnchor() < nextNode.getYAnchor():
                            node.adjustY(-0.2)
                    elif isinstance(thisOverlapNode, OverlapNode) and not (isinstance(nextOverlapNode, OverlapNode)):
                        if nextNode.getXAnchor() >= node.getXAnchor():
                            nextNode.adjustX(0.2)
                        elif nextNode.getXAnchor() < node.getXAnchor():
                            nextNode.adjustX(-0.2)

                        if nextNode.getYAnchor() >= node.getYAnchor():
                            nextNode.adjustY(0.2)
                        elif nextNode.getXAnchor() < node.getYAnchor():
                            nextNode.adjustY(-0.2)
                    elif not (isinstance(thisOverlapNode, OverlapNode)) and not (isinstance(nextOverlapNode, OverlapNode)):
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

        print("---- Move on ---")
        i = i + 1
    
    aloneNodeLengthList = []
    for node in aloneNodeList:
        aloneNodeLengthList.append(node.getNodeWidth())
    if len(aloneNodeLengthList) != 0:
        mapRadius = overlappedRadius + max(aloneNodeLengthList)
    else:
        mapRadius = overlappedRadius
    
    return([-mapRadius, mapRadius])

def findOverlapNode(overlapNodeList, name):
    for overlapNode in overlapNodeList:
        if name == overlapNode.getName():
            return overlapNode