from overlapNode import OverlapNode
import math

# Calculate node positions of a overlapNode
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

# Calculate node positions of a overlapNode Pair
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


def calOverlapLayout(graph):
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
        calPairedPositions(overlapPair, initialCenter)

        count = count - 1

    # Calculate the positions of un-paired-overlapped nodes
    overlapUnpairNum = len(overlapUnpairList)

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
            calNodePosition(overlapUnpair, 0)
            i = i + 1

            for node in overlapUnpair.getNodesContain():
                overlapUnpairNodeLengthList.append(node.getNodeWidth())

    # Calculate the positions of alone nodes
    aloneNodeNum = len(aloneNodeList)
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
    