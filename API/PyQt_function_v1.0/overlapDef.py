from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

from overlap.graph import Graph
from overlap.layoutAlgorithmOverlap import calOverlapLayout
from overlap.overlapPatten import pattern2Draw


def figureCub():
    return figure(facecolor="blue")


# return figure to canvas
def figureCirc():
    graphDemo = Graph()
    graphDemo.readInput("resource/sample_input.txt", 2)  # represent pattern 2
    calOverlapLayout(graphDemo, 2)  # represent pattern 2

    f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
    f.subplots_adjust(hspace=0, wspace=0)

    pattern2Draw(graphDemo, ax1)

    plt.grid(False)
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)

    return plt.gcf()


# close the plt
def figureDel(plt):
    plt.close()  # from matplotlib.pyplot import close
