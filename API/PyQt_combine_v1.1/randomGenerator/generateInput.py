# The generated input is completely random and there will not have repeated literals

from math import log10, exp, log2
from string import ascii_uppercase
from random import randint


def generateInput(seed: int):
    # Keep all the literals generated to avoid repetition
    literalsGenerated = []
    # Keep all the nodes generated
    nodesGenerated = []
    # The sum of all the digits in seed
    digitSum = seed//10000 + (seed % 10000)//1000 + \
        (seed % 1000)//100 + (seed % 100)//10 + (seed % 10)
    # Input
    input = ""

    #-----Start the process of generating parameters-----#
    # Firstly determine the number of overlapping literals (1 or 2)
    overlappingLiteralsNum = digitSum*digitSum % 2 + 1
    # Then determine the number of overlapped supernodes with two overlaps (1 or 2 or 3)
    twoOverlapSupernodesNum = int(digitSum*seed*digitSum**0.5) % 3 + 1
    # Then determine the number of overlapped supernodes with three overlaps (0 or 1 or 2)
    threeOverlapSupernodesNum = int(log10(digitSum*seed*digitSum**0.6)) % 3 + 1
    # Finally determine the number of single nodes (5 or 6 or 7 or 8 or 9 or 10)
    singleNodesNum = int(exp(log2(digitSum*seed*digitSum**0.6))) % 6 + 5

    #-----Start the process of generating input-----#
    # Firstly generate overlapped supernodes with two overlaps
    for i in range(twoOverlapSupernodesNum):
        overlappingLiteralsLeft = []
        overlappingLiteralsRight = []
        mainNode = []
        groupLeft = []
        groupRight = []

        # Generate the main node
        for m in range(randint(7, 9)):
            literal = generateUniqueLiteral(literalsGenerated)
            literalsGenerated.append(literal)
            mainNode.append(literal)
        nodesGenerated.append(listToStr(mainNode))

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
                literal = generateUniqueLiteral(literalsGenerated)
                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupLeft.append(tempNode)
            nodesGenerated.append(tempNode)

        # Generate the subnodes in the right
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsRight)

            for sub in range(randint(1, 3)):
                literal = generateUniqueLiteral(literalsGenerated)
                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupRight.append(tempNode)
            nodesGenerated.append(tempNode)

        # Print to the input
        input = input + groupToStr(groupLeft, listToStr(mainNode)) + " "
        input = input + groupToStr(groupRight,
                                   listToStr(reverseList(mainNode))) + " "

    # Secondly generate overlapped nodes with three overlaps
    for i1 in range(threeOverlapSupernodesNum):
        overlappingLiteralsLeft = []
        overlappingLiteralsRight = []
        overlappingLiteralsMiddle = []
        mainNode = []
        groupLeft = []
        groupRight = []
        groupMiddle = []

        # Generate the main node
        for m1 in range(randint(8, 10)):
            literal = generateUniqueLiteral(literalsGenerated)
            literalsGenerated.append(literal)
            mainNode.append(literal)
        nodesGenerated.append(listToStr(mainNode))

        # Generate the left and right overlapping literals
        overlappingLiteralsLeft = mainNode[0:overlappingLiteralsNum]
        overlappingLiteralsRight = reverseList(
            mainNode)[0:overlappingLiteralsNum]
        overlappingLiteralsMiddle = mainNode[len(
            mainNode)//2 - 1:len(mainNode)//2 - 1 + overlappingLiteralsNum]

        # Generate the subnodes in the left
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsLeft)

            for sub in range(randint(2, 5)):
                literal = generateUniqueLiteral(literalsGenerated)
                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupLeft.append(tempNode)
            nodesGenerated.append(tempNode)

        # Generate the subnodes in the right
        for node in range(randint(1, 3)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsRight)

            for sub in range(randint(2, 5)):
                literal = generateUniqueLiteral(literalsGenerated)
                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupRight.append(tempNode)
            nodesGenerated.append(tempNode)

        # Generate the subnodes in the middle
        for node in range(randint(1, 2)):
            tempNode = ""
            tempNode = tempNode + listToStr(overlappingLiteralsMiddle)

            for sub in range(randint(3, 5)):
                literal = generateUniqueLiteral(literalsGenerated)
                literalsGenerated.append(literal)
                tempNode = tempNode + literal

            groupMiddle.append(tempNode)
            nodesGenerated.append(tempNode)

        # Print to the input
        input = input + groupToStr(groupLeft, listToStr(mainNode)) + " "
        input = input + groupToStr(groupRight,
                                   listToStr(reverseList(mainNode))) + " "
        input = input + groupToStr(groupMiddle,
                                   listToStr(reorganizeList(mainNode, len(
                                       mainNode)//2 - 1, overlappingLiteralsNum))) + " "

    # Thirdly generate single nodes
    for s1 in range(singleNodesNum):
        tempNode = ""
        # The number of literals in a node
        for node in range(5, 8):
            literal = generateUniqueLiteral(literalsGenerated)
            literalsGenerated.append(literal)
            tempNode = tempNode + literal

        input = input + tempNode + " "

    input = input[0:-1] + "\n"

    # Finally generate edges
    nodesNum = len(nodesGenerated)
    for i in range(0, nodesNum):
        for j in range(i, nodesNum):
            # 10% of possibility
            randomNum = randint(1, 10)
            if randomNum == 6:
                input = input + nodesGenerated[i] + \
                    " " + nodesGenerated[j] + "\n"

    input = partiallyDeleteDigits(input)
    # Print input to the file
    printToFile(input)


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
    fileHandler = open("resource/random_input.txt", "w")
    fileHandler.write(input)
    fileHandler.close()
    
def deleteDigits(input):
    input = input.replace('0','')
    input = input.replace('1','')
    input = input.replace('2','')
    input = input.replace('3','')
    input = input.replace('4','')
    input = input.replace('5','')
    input = input.replace('6','')
    input = input.replace('7','')
    input = input.replace('8','')
    input = input.replace('9', '')
    return input

def partiallyDeleteDigits(input):
    flagInitial = True
    i = 0

    while True:
        if i == len(input):
            break

        if flagInitial == True:
            if input[i].isdigit():
                input = input[0:i]+input[i+1:]
                i = i-1

        if input[i] == '_':
            flagInitial = False
            input = input[0:i+2]+input[i+3:]

        if input[i] == ' ':
            flagInitial = True
            if input[i:].find('_') == -1:
                flagInitial = False

        if input[i] == '\n':
            input = input[0:i]
            break

        i = i+1

    return input


if __name__ == '__main__':
    generateInput(52732)
    # generateInput(22133)
    # print(reorganizeList([1, 2, 3, 4], 1, 2))
