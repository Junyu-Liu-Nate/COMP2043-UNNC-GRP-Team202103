from node import Node
from overlapNode import OverlapNode


class Graph:

    def __init__(self):
        # In the form like: [AB, BC_BH_BF, KL], all Node or OverlapNode objects
        # AB, KL stands for separate nodes, while BC_BH_BF stands for a group of overlapped nodes
        # AB, KL are Node types, while BC_BH_BF is OverlapNode type which is the subtype of Node
        self.__nodeList = []
        self.__edgeList = []

    def readInput(self, fileName):
        with open("inputs/" + fileName, "r") as fileHandler:
            # Read nodes
            # 读取一行，这一行包含了所有的node的名字 例：AB_AC_AD E F G
            # 这其中，AB_AC_AD表示这是一个由三个小node overlap后组成的大node，而E,F,G则是三个单独的node
            tempTxt = fileHandler.readline()
            # Split the line using space
            tempNodeList = tempTxt.split()
            for tempNode in tempNodeList:
                # overlap后的大node放到一个OverlapNode对象中，这个对象中包含了一个List，list中是这个大node中包含的所有小node，小node是Node对象
                # Initialise the overlapped node
                if '_' in tempNode:
                    self.__nodeList.append(OverlapNode(tempNode))
                # 单独的node放到一个Node对象中，其中包含了画出它时需要用到的三个信息
                else:
                    self.__nodeList.append(Node(tempNode))

            # Read edges
            for edge in fileHandler.readlines():
                self.__edgeList.append(edge.split())

    # Find and return Node instance through name
    def findNode(self, nodeName: str):
        length = len(self.__nodeList)
        for i in range(0, length):
            tempNode = self.__nodeList[i]

            if isinstance(tempNode, Node):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode
                else:
                    continue

            if isinstance(tempNode, OverlapNode):
                if tempNode.getName().find(nodeName) != -1:
                    return tempNode.findSubNode(nodeName)
                else:
                    continue


# TEMPORARY CODE #
a = Graph()
a.readInput("sample_input.txt")
b = a.findNode("ACD")
print(b.getName())
