from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

from overlap.graph import Graph
from overlap.layoutAlgorithmOverlap import calOverlapLayout
from overlap.overlapPatten import pattern1Draw, pattern2Draw


# return figure to canvas
def figurePrint():
    with open("resource/sample_input.txt", "r") as patternSeclect:
        if (patternSeclect.read(1) == '#'):
            patternNum = 1
        else:
            patternNum = 2
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", patternNum)
    windowRange = calOverlapLayout(graphDemo, patternNum)
    zoomRatio = windowRange[1] / 6
    if zoomRatio == 0:
        zoomRatio = 1

    # ----- Draw Overlapped Layout Graph -----#
    # Specify the size of figure window
    f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    if patternNum == 1:
        pattern1Draw(graphDemo, ax1, zoomRatio)
    else:
        pattern2Draw(graphDemo, ax1, zoomRatio)

    plt.grid(False)
    ax1.set_xlim(windowRange[0], windowRange[1])
    ax1.set_ylim(windowRange[0], windowRange[1])

    return plt.gcf()

def printCub():
    patternNum = 1
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", patternNum)
    windowRange = calOverlapLayout(graphDemo, patternNum)
    zoomRatio = windowRange[1] / 6
    if zoomRatio == 0:
        zoomRatio = 1

    # ----- Draw Overlapped Layout Graph -----#
    # Specify the size of figure window
    f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    if patternNum == 1:
        pattern1Draw(graphDemo, ax1, zoomRatio)
    else:
        pattern2Draw(graphDemo, ax1, zoomRatio)

    plt.grid(False)
    ax1.set_xlim(windowRange[0], windowRange[1])
    ax1.set_ylim(windowRange[0], windowRange[1])

    return plt.gcf()

def printCirc():
    patternNum = 2
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", patternNum)
    windowRange = calOverlapLayout(graphDemo, patternNum)
    zoomRatio = windowRange[1] / 6
    if zoomRatio == 0:
        zoomRatio = 1

    # ----- Draw Overlapped Layout Graph -----#
    # Specify the size of figure window
    f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    if patternNum == 1:
        pattern1Draw(graphDemo, ax1, zoomRatio)
    else:
        pattern2Draw(graphDemo, ax1, zoomRatio)

    plt.grid(False)
    ax1.set_xlim(windowRange[0], windowRange[1])
    ax1.set_ylim(windowRange[0], windowRange[1])

    return plt.gcf()

# close the plt
def figureDel(plt):
    plt.close()  # from matplotlib.pyplot import close
