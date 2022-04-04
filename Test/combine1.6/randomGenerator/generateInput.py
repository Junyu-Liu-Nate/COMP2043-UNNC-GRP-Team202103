# The generated input is completely random and there will not have repeated literals

from math import log10, exp, log2
from string import ascii_uppercase
from random import randint


def generateInput(seed: int):
    # Keep all the literals generated to avoid repetition
    literalsGenerated = []
    # Keep all the overlap nodes generated (Because two overlap nodes cannot contain exactly the same literals)
    overlapGenerated = []
    # Keep all the nodes generated
    nodesGenerated = []
    nodesGeneratedInGroups = []
    # The sum of all the digits in seed
    digitSum = seed // 10000 + (seed % 10000) // 1000 + \
        (seed % 1000) // 100 + (seed % 100) // 10 + (seed % 10)
    # Input
    input = ""

    # -----Start the process of generating parameters-----#
    # Firstly determine the number of overlapping literals (1 or 2)
    overlappingLiteralsNum = digitSum * digitSum % 2 + 1
    # Then determine the number of overlapped supernodes with two overlaps (1 or 2 or 3)
    twoOverlapSupernodesNum = int(digitSum * seed * digitSum ** 0.5) % 3 + 1
    # Then determine the number of overlapped supernodes with three overlaps (0 or 1 or 2)
    threeOverlapSupernodesNum = int(
        log10(digitSum * seed * digitSum ** 0.6)) % 3 + 1
    # Finally determine the number of single nodes (5 or 6 or 7 or 8 or 9 or 10)
    singleNodesNum = int(exp(log2(digitSum * seed * digitSum ** 0.6))) % 6 + 5

    if overlappingLiteralsNum == 1:
        input = "#\n" + input
    elif overlappingLiteralsNum == 2:
        input = "%\n" + input

    # -----Start the process of generating input-----#
    # Firstly generate overlapped supernodes with two overlaps
    for i in range(twoOverlapSupernodesNum):
        # Keep all the generated alphas
        alphaGenerated = []
        overlappingLiteralsLeft = []
        overlappingLiteralsRight = []
        mainNode = []
        groupLeft = []
        groupRight = []
        tempNodesGenerated = []

        # Generate the main node
        flag = False
        while not flag:
            tempAlphaGenerated = []
            tempMainNode = []
            for m in range(randint(7, 9)):
                alpha = generateUniqueAlpha(tempAlphaGenerated)
                tempAlphaGenerated.append(alpha)
                tempMainNode.append(alpha)

            flag = listToStr(tempMainNode) not in overlapGenerated

        alphaGenerated += tempAlphaGenerated
        mainNode += tempMainNode
        nodesGenerated.append(listToStr(mainNode))
        overlapGenerated.append(listToStr(mainNode))
        tempNodesGenerated.append(listToStr(mainNode))

        # Generate the left and right overlapping literals
        overlappingLiteralsLeft = mainNode[0:overlappingLiteralsNum]
        overlappingLiteralsRight = reverseList(
            mainNode)[0:overlappingLiteralsNum]

        # Generate the subnodes in the left
        # Number of nodes
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsLeft)

            # Number of literals in a single node
            for sub in range(randint(1, 3)):
                flag = False
                while not flag:
                    literal = generateUniqueLiteral(literalsGenerated)
                    flag = literal[0] not in alphaGenerated

                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupLeft.append(tempNode)
            nodesGenerated.append(tempNode)
            tempNodesGenerated.append(tempNode)

        # Generate the subnodes in the right
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsRight)

            for sub in range(randint(1, 3)):
                flag = False
                while not flag:
                    literal = generateUniqueLiteral(literalsGenerated)
                    flag = literal[0] not in alphaGenerated

                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupRight.append(tempNode)
            nodesGenerated.append(tempNode)
            tempNodesGenerated.append(tempNode)

        # Print to the input
        input = input + groupToStr(groupLeft, listToStr(mainNode)) + " "
        input = input + groupToStr(groupRight,
                                   listToStr(reverseList(mainNode))) + " "
        nodesGeneratedInGroups.append(tempNodesGenerated)

    # Secondly generate overlapped nodes with three overlaps
    for i1 in range(threeOverlapSupernodesNum):
        # Keep all the generated alphas
        alphaGenerated = []
        overlappingLiteralsLeft = []
        overlappingLiteralsRight = []
        overlappingLiteralsMiddle = []
        mainNode = []
        groupLeft = []
        groupRight = []
        groupMiddle = []
        tempNodesGenerated = []

        # Generate the main node
        flag = False
        while not flag:
            tempAlphaGenerated = []
            tempMainNode = []
            for m1 in range(randint(8, 10)):
                alpha = generateUniqueAlpha(tempAlphaGenerated)
                tempAlphaGenerated.append(alpha)
                tempMainNode.append(alpha)

            flag = listToStr(tempMainNode) not in overlapGenerated

        alphaGenerated += tempAlphaGenerated
        mainNode += tempMainNode
        nodesGenerated.append(listToStr(mainNode))
        overlapGenerated.append(listToStr(mainNode))
        tempNodesGenerated.append(listToStr(mainNode))

        # Generate the left and right overlapping literals
        overlappingLiteralsLeft = mainNode[0:overlappingLiteralsNum]
        overlappingLiteralsRight = reverseList(
            mainNode)[0:overlappingLiteralsNum]
        overlappingLiteralsMiddle = mainNode[len(
            mainNode) // 2 - 1:len(mainNode) // 2 - 1 + overlappingLiteralsNum]
        overlappingLiteralsMiddle = reverseList(overlappingLiteralsMiddle)

        # Generate the subnodes in the left
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsLeft)

            for sub in range(randint(2, 5)):
                flag = False
                while not flag:
                    literal = generateUniqueLiteral(literalsGenerated)
                    flag = literal[0] not in alphaGenerated

                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupLeft.append(tempNode)
            nodesGenerated.append(tempNode)
            tempNodesGenerated.append(tempNode)

        # Generate the subnodes in the right
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsRight)

            for sub in range(randint(2, 5)):
                flag = False
                while not flag:
                    literal = generateUniqueLiteral(literalsGenerated)
                    flag = literal[0] not in alphaGenerated

                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupRight.append(tempNode)
            nodesGenerated.append(tempNode)
            tempNodesGenerated.append(tempNode)

        # Generate the subnodes in the middle
        for node in range(randint(1, 2)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsMiddle)

            for sub in range(randint(3, 5)):
                flag = False
                while not flag:
                    literal = generateUniqueLiteral(literalsGenerated)
                    flag = literal[0] not in alphaGenerated

                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupMiddle.append(tempNode)
            nodesGenerated.append(tempNode)
            tempNodesGenerated.append(tempNode)

        # Print to the input
        input = input + groupToStr(groupLeft, listToStr(mainNode)) + " "
        input = input + groupToStr(groupRight,
                                   listToStr(reverseList(mainNode))) + " "
        ###########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################################
        if overlappingLiteralsNum == 2:
            mainNodeA = mainNode[0:len(mainNode) // 2 - 1]
            tempA = [mainNode[len(mainNode) // 2 - 1]]
            tempB = [mainNode[len(mainNode) // 2]]
            mainNodeB = mainNode[len(mainNode) // 2+1:]
            mainNode = mainNodeA+tempB+tempA+mainNodeB
        ###########################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!######################################
        input = input + groupToStr(groupMiddle,
                                   listToStr(reorganizeList(mainNode, len(
                                       mainNode) // 2 - 1, overlappingLiteralsNum))) + " "
        nodesGeneratedInGroups.append(tempNodesGenerated)

    # Thirdly generate single nodes
    for s1 in range(singleNodesNum):
        tempNode = ""
        # The number of literals in a node
        for node in range(5, 8):
            literal = generateUniqueLiteral(literalsGenerated)
            literalsGenerated.append(literal)
            tempNode = tempNode + literal

        input = input + tempNode + " "
        tempNodeInList = [tempNode]
        nodesGeneratedInGroups.append(tempNodeInList)

    input = input[0:-1] + "\n"

    # Finally generate edges
    input = generateAdjacentEdge(input, nodesGeneratedInGroups, 2)
    # input = partiallyDeleteDigits(input)
    # Print input to the file
    printToFile(input)

# Generate edge randomly, may cause lots of overlapping between nodes and edges


def randomlyGenerateEdge(input, nodesGenerated):
    nodesNum = len(nodesGenerated)
    for i in range(0, nodesNum):
        for j in range(i, nodesNum):
            # 10% of possibility
            randomNum = randint(1, 10)
            if randomNum == 1:
                input = input + nodesGenerated[i] + \
                    " " + nodesGenerated[j] + "\n"

    return input


# possibility == 10 means 1/10(10%)
def generateAdjacentEdge(input, nodesGeneratedInGroups, possibility):
    individualNodesStartIndex = 0
    for i in range(0, len(nodesGeneratedInGroups)):
        if len(nodesGeneratedInGroups[i]) == 1:
            individualNodesStartIndex = i
            break

        group = nodesGeneratedInGroups[i]
        leftOverlapNodeIndex = 1
        rightOverlapNodeIndex = 0
        endIndex = len(group)-1
        # -1 means it does not contain a middle overlapping
        middleOverlapNodeIndex = -1
        tempLiteral = ''
        for nodeIndex in range(0, len(group)):
            node = group[nodeIndex]
            thisLiteral = node[0]
            if tempLiteral == '':
                tempLiteral = thisLiteral
                continue
            elif tempLiteral == thisLiteral:
                continue
            elif tempLiteral != thisLiteral:
                if rightOverlapNodeIndex == 0:
                    rightOverlapNodeIndex = nodeIndex
                else:
                    middleOverlapNodeIndex = nodeIndex

        # Generate edges for left overlapping group
        # Which means there is more than 1 node in the left group
        if leftOverlapNodeIndex+1 < rightOverlapNodeIndex:
            for i in range(leftOverlapNodeIndex, rightOverlapNodeIndex-1):
                randomNum = randint(1, possibility)
                if randomNum == 1:
                    input += group[i] + " " + group[i+1] + "\n"

        # Which means there is no overlapping in the middle
        if middleOverlapNodeIndex == -1:
            if rightOverlapNodeIndex < endIndex:
                for i in range(rightOverlapNodeIndex, endIndex):
                    randomNum = randint(1, possibility)
                    if randomNum == 1:
                        input += group[i] + " " + group[i+1] + "\n"
        # There is overlapping in the middle
        else:
            if rightOverlapNodeIndex+1 < middleOverlapNodeIndex:
                for i in range(rightOverlapNodeIndex, middleOverlapNodeIndex-1):
                    randomNum = randint(1, possibility)
                    if randomNum == 1:
                        input += group[i] + " " + group[i+1] + "\n"
            if middleOverlapNodeIndex < endIndex:
                for i in range(middleOverlapNodeIndex, endIndex):
                    randomNum = randint(1, possibility)
                    if randomNum == 1:
                        input += group[i] + " " + group[i+1] + "\n"

        # Generate edges between mainNode and subNodes
        for i in range(1, endIndex+1):
            randomNum = randint(1, possibility)
            if randomNum == 1:
                input += group[0] + " " + group[i] + "\n"

    # Generate edges between overlap nodes
    for i in range(0, individualNodesStartIndex):
        randomNum = randint(1, possibility)
        if randomNum == 1:
            input += nodesGeneratedInGroups[i][0] + \
                " " + nodesGeneratedInGroups[i+1][0] + "\n"

    # Generate edges between individual nodes
    for i in range(individualNodesStartIndex, len(nodesGeneratedInGroups)-1):
        randomNum = randint(1, possibility)
        if randomNum == 1:
            input += nodesGeneratedInGroups[i][0] + \
                " " + nodesGeneratedInGroups[i+1][0] + "\n"

    return input


# Function used to generate an unique literal which is not in 'literalGenerated'
def generateUniqueLiteral(literalsGenerated):
    while True:
        literal = ascii_uppercase[randint(0, 25)] + str(randint(0, 9))
        if literal not in literalsGenerated:
            return literal


def listToStr(literalList):
    nodeStr = ""
    for literal in literalList:
        nodeStr = nodeStr + literal

    return nodeStr


def groupToStr(group, mainNode: str):
    nodeStr = "" + mainNode + "_"
    for literal in group:
        nodeStr = nodeStr + literal + "_"

    return nodeStr[0:-1]


def reverseList(lst):
    return [ele for ele in reversed(lst)]


# Given the position and number of overlap literals, place the overlap literals in front of the list
def reorganizeList(lst, pos, overlappingLiteralsNum):
    tempList = []
    for i in range(overlappingLiteralsNum):
        tempList.append(lst.pop(pos))

    return tempList + lst


def printToFile(input):
    fileHandler = open("resource/sample_input.txt", "w")
    fileHandler.write(input)
    fileHandler.close()


def generateUniqueAlpha(alphaGenerated):
    while True:
        alpha = ascii_uppercase[randint(0, 25)]
        if alpha not in alphaGenerated:
            return alpha


def deleteDigits(input):
    input = input.replace('0', '')
    input = input.replace('1', '')
    input = input.replace('2', '')
    input = input.replace('3', '')
    input = input.replace('4', '')
    input = input.replace('5', '')
    input = input.replace('6', '')
    input = input.replace('7', '')
    input = input.replace('8', '')
    input = input.replace('9', '')
    return input


def partiallyDeleteDigits(input):
    flagInitial = True
    i = 2

    while True:
        if i == len(input):
            break

        if flagInitial == True:
            if input[i].isdigit():
                input = input[0:i] + input[i + 1:]
                i = i - 1

        if input[i] == '_':
            flagInitial = False
            input = input[0:i + 2] + input[i + 3:]

        if input[i] == ' ':
            flagInitial = True
            if input[i:].find('_') == -1:
                flagInitial = False

        if input[i] == '\n':
            input = input[0:i]
            break

        i = i + 1

    return input


if __name__ == '__main__':
    generateInput(52732)
    # generateInput(22133)
    # print(reorganizeList([1, 2, 3, 4], 1, 2))
