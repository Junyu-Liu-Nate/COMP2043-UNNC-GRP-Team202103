from overlapNode import OverlapNode
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

    overlapNode1.setxCenter(initialCenter[0])
    overlapNode1.setyCenter(initialCenter[1])
    calNodePosition(overlapNode1, 0)

    pairNode = overlapNode1.findSubNode(pairNodeName)
    pairNodeEnd2 = pairNode.getEnd2Coordinate()
    overlapNode2.setxCenter(pairNodeEnd2[0])
    overlapNode2.setyCenter(pairNodeEnd2[1])
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

    # Seperate paired-overlapped nodes from overlapped nodes
    overlapPairList = []
    i = 0
    for overlapNode in overlapNodeList:
        nodeList = overlapNode.getNodesContain()

        if i < len(overlapNodeList) - 1:
            for node in nodeList:
                for nextOverlapNode in overlapNodeList[i:]:
                    if nextOverlapNode.checkIsPaired():
                        continue
                    nextNodeList = nextOverlapNode.getNodesContain()
                    for nextNode in nextNodeList:
                        if node.getName() == nextNode.getName()[::-1]:
                            overlapNode.setIsPaired(True)
                            overlapNode.setPairedNode(node)
                            nextOverlapNode.setIsPaired(True)
                            nextOverlapNode.setPairedNode(node)
                            overlapPairList.append([overlapNode, nextOverlapNode])
        i = i + 1

    # Seperate un-paired-overlapped nodes from overlapped nodes
    overlapUnpairList = []
    for overlapNode in overlapNodeList:
        if overlapNode.checkIsPaired() == False:
            overlapUnpairList.append(overlapNode)

    mapCenter = [0,0]

    # Calculate the positions of paired-overlapped nodes
    overlapPairNum = len(overlapPairList)
    count = overlapPairNum / 2 - 0.5
    overlapPairHeightList = []
    for overlapPair in overlapPairList:
        overlapNode1Radius = overlapPair[0].getRadius()
        overlapNode2Radius = overlapPair[1].getRadius()
        overlapPairWidth = overlapNode1Radius + overlapNode2Radius
        # overlapPairHeight = max([overlapNode1Radius, overlapNode2Radius])
        overlapPairHeight = overlapNode1Radius + overlapNode2Radius
        overlapPairHeightList.append(overlapPairHeight)

        initialCenter = [mapCenter[0] - overlapPairWidth / 4, mapCenter[1] + overlapPairHeight * count]
        #initialCenter = [0,0]

        if patternNum == 1:
            calPairedPositions(overlapPair, initialCenter)
        else:
            calPairedPositions2(overlapPair, initialCenter)
        
        count = count - 1

    # Calculate the positions of un-paired-overlapped nodes
    overlapUnpairNum = len(overlapUnpairList)

    if overlapUnpairNum != 0:
        if sum(overlapPairHeightList) >= overlapPairWidth:
            pairedRadius = sum(overlapPairHeightList) / 2 + 8 # !!! NEED further calculation !!!
        else:
            pairedRadius = overlapPairWidth + 8 # !!! NEED further calculation !!!

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
    if aloneNodeNum != 0:
        #print(pairedRadius)
        overlappedRadius = pairedRadius + max(overlapUnpairNodeLengthList) + 8
        #print(overlappedRadius)
        i = 0
        rotateRate = 360 / aloneNodeNum

        for node in aloneNodeList:
            rotateAngle = rotateRate * i
            center = [mapCenter[0] + overlappedRadius * math.cos(math.radians(rotateAngle)), overlappedRadius * math.sin(math.radians(rotateAngle))]
            node.adjustX(center[0])
            node.adjustY(center[1])

            i = i + 1