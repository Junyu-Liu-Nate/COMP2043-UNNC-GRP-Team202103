from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

from overlap.graph import Graph
from overlap.layoutAlgorithmOverlap import calOverlapLayout
from overlap.overlapPatten import pattern1Draw, pattern2Draw
from overlap.layoutAlgorithmOriginal import calLayout


# return figure to canvas
def figurePrint(patternNum):
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", patternNum)

    # Calculate the original layout
    windowRange = calLayout(graphDemo)
    zoomRatio = windowRange / 6

    f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    pattern1Draw(graphDemo, ax1, zoomRatio)

    plt.grid(False)
    ax1.set_xlim(-windowRange, windowRange)
    ax1.set_ylim(-windowRange, windowRange)
    plt.savefig("resource/beforeFig.png")
    plt.cla()

    # Calculate the layout after overlapping
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", patternNum)

    windowRange = calOverlapLayout(graphDemo, patternNum)
    zoomRatio = windowRange[1] / 6
    if zoomRatio == 0:
        zoomRatio = 1

    # ----- Draw Overlapped Layout Graph -----#
    # Specify the size of figure window
    f, (ax2) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    if patternNum == 1:
        pattern1Draw(graphDemo, ax2, zoomRatio)
    else:
        pattern2Draw(graphDemo, ax2, zoomRatio)

    plt.grid(False)
    ax2.set_xlim(windowRange[0], windowRange[1])
    ax2.set_ylim(windowRange[0], windowRange[1])

    plt.savefig("resource/afterFig.png")
    return plt.gcf()
