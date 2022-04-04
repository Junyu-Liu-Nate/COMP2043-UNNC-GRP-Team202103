    def generateInput(seed: int):
        """
        Genertae input from seed
        :param seed: a number which stands for the seed
        :return: no return
        """

    def randomlyGenerateEdge(input, nodesGenerated):
        """
        Generate edge randomly, may cause lots of overlapping between nodes and edges
        :param input: the input file
        :param nodesGenerated: the generated nodes
        :return: the input file with edge added
        """

    def generateAdjacentEdge(input, nodesGeneratedInGroups, possibility):
        """
        Generate edges for adjacent nodes
        :param input: the input file
        :param nodesGeneratedInGroups: the nodes that are grouped together
        :param possibility: the possiblity of generating edges
        :return: the input file with edge added
        """

    def generateUniqueLiteral(literalsGenerated):
        """
        Function used to generate an unique literal which is not in 'literalGenerated'
        :param literalsGenerated: literals that are already generated
        :return: generated literals
        """

    def listToStr(literalList):
        """
        Convert a list to a string
        :param literalList: a list of strings
        :return: the connected string
        """

    def groupToStr(group, mainNode: str):
        """
        Convert a group of node names into a string
        :param group: a group of node names
        :param mainNode: the main node
        :return: a string that connects a group of node names into a string
        """

    def reverseList(lst):
        """
        Reverse a list
        :param lst: a list
        :return: a list with the order reversed
        """

    def reorganizeList(lst, pos, overlappingLiteralsNum):
        """
        Given the position and number of overlap literals, place the overlap literals in front of the list
        :param lst: a list
        :param pos: a position
        :param overlappingLiteralsNum: the number of overlapping literals number
        :return: a reorganized list
        """

    def printToFile(input):
        """
        Print to a file
        :param input: the generated input file
        :return: no return
        """

    def generateUniqueAlpha(alphaGenerated):
        """
        Generate a unique alphabet
        :param alphaGenerated: a unique alphabet
        :return: a unique alphabet
        """

    def deleteDigits(input):
        """
        Delete digits in a file
        :param input: a given input file
        :return: the input file with digits deleted
        """

    def partiallyDeleteDigits(input):
        """
        Partially delete digits in a file
        :param input: a given input file
        :return: the input file with digits partially deleted
        """