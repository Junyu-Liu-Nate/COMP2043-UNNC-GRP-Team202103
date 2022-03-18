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
    currentRadius = 0.7
    centerDistance = math.sqrt(currentRadius * currentRadius - pairNodeHeight * pairNodeHeight / 4) * 2 + pairNodeWidth

    overlapNode1Center = overlapNode1.getCenter()
    overlapNode2.setxCenter(overlapNode1Center[0] + centerDistance * math.cos(math.radians(pairNodeAngle)))
    overlapNode2.setyCenter(overlapNode1Center[1] + centerDistance * math.sin(math.radians(pairNodeAngle)))

    angle2 = pairNode.getAngle()
    calNodePosition2(overlapNode2, angle2 - 180)


def findConnectionNode(overlapNode):
    for node in overlapNode.getNodesContain():
        if node.checkIsConnected() == True:
            return node

def calGroupPosition1(overlapGroup, initialCenter):
    overlapNodeList = overlapGroup.getOverlapNodeList()
    print("There are " + str(len(overlapNodeList)) + " in this overlapGroup")
    overlapNodeName = overlapGroup.getOverlapNodeName()

    if len(overlapNodeList) == 2:
        overlapNode1 = overlapNodeList[0]
        overlapNode2 = overlapNodeList[1]

        overlapNode1.setPairedNode(findConnectionNode(overlapNode1))
        #print(findConnectionNode(overlapNode1).getName())
        overlapNode2.setPairedNode(findConnectionNode(overlapNode2))
        #print(findConnectionNode(overlapNode2).getName())
        print(overlapNode1.getPairedNode().getName())
        print(overlapNode2.getPairedNode().getName())

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
                        if sorted(node.getName()) == sorted(nextNode.getName()):
                            overlapNode.setIsPaired(True)
                            nextOverlapNode.setIsPaired(True)
                            node.setIsConnected(True)
                            nextNode.setIsConnected(True)

                            overlapNodeGroup.append(nextOverlapNode)
                            print([sorted(node.getName()), sorted(nextNode.getName())])

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
    print("overlapGroup number is " + str(overlapGroupNum))
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

    for overlapGroup in overlapGroupList:
        overlapNode1Radius = overlapGroup.getOverlapNodeList()[0].getRadius()
        overlapNode2Radius = overlapGroup.getOverlapNodeList()[1].getRadius()
        overlapPairWidth = overlapNode1Radius + overlapNode2Radius

        overlapPairHeight = overlapNode1Radius + overlapNode2Radius
        overlapPairHeightList.append(overlapPairHeight)

        #initialCenter = [mapCenter[0] - overlapPairWidth / 4, mapCenter[1] + overlapPairHeight * count]
        #initialCenter = [0 - overlapPairWidth / 4, 0 + overlapPairHeight * count]
        #print(initialCenter)
        initialCenter = [0,0]

        if patternNum == 1:
            # calPairedPositions(overlapGroup, initialCenter)
            calGroupPosition1(overlapGroup, initialCenter)
        else:
            calPairedPositions2(overlapGroup, initialCenter)
        
        count = count - 1

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