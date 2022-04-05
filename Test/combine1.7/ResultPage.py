import PyQt5
import PyQt5.Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QUrl, QFileInfo
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QFileDialog, QSplitter, QButtonGroup, QMessageBox, QApplication, QGridLayout
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import overlapDef
from overlap.graph import Graph
from overlap.layoutAlgorithmOverlap import calOverlapLayout
from overlap.overlapPatten import pattern1Draw, pattern2Draw
from widgetsCreator import createLabPix, createToolBtn, createRadioBtn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class resultPage(QWidget):
    """
    The class offers the paradigm of the result page of the program,
    including the original overlap result and def calls of functions:
    switch pages of the window to see the difference before and after overlap,
    alter overlap style, zoom and drag the result figure,
    export result image and return the enter page.
    Class variables: self.stackedWidget helps to switch page contents,
    self.btnSR helps to confirm the first page is shown every time result page is shown,
    self.layoutSR, self.figureSR and self.canvasSR help to change the content of show result page,
    self.layoutFB and self.webFB help tp refresh the content of feedback page
    self.patternNum helps to change the alter overlap style,
    self.inputChoice helps to record the available choices of overlap style for one input file,
    self.btnASCub and self.btnASCirc help to deliver alter style information,
    self.toolBar helps to link the figure pan function with the canvas.
    """
    sign_toEnter = pyqtSignal()

    def __init__(self):
        """
        The def to initialize the enter page QWidget window
        """
        super(resultPage, self).__init__()
        self.figureSR = None
        self.inputChoice = None
        self.webFB = None
        self.layoutFB = None
        self.btnASCirc = None
        self.btnASCub = None
        self.layoutSD = None
        self.layoutSR = None
        self.btnSR = None
        self.stackedWidget = None
        self.patternNum = None
        desktop = QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        self.resize(int(width / 1.5), int(height / 1.5))
        self.setWindowTitle("OVERLAP")

        pixIcon = PyQt5.QtGui.QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)
        self.setWindowIcon(iconEP)

        # add CSS styles to the page
        with open("resource/styleSettings.txt", "r") as self.style:
            textOfStyle = self.style.read()
            self.setStyleSheet(textOfStyle)
            self.style.close()

        self.initUI()

    def initUI(self):
        """
        Initialize the main page settings
        :return: None
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        layoutBtn = QHBoxLayout()
        self.stackedWidget = QStackedWidget()

        splitter = QSplitter(QtCore.Qt.Horizontal)
        layout.addLayout(layoutBtn, 150)
        layout.addWidget(splitter, 2)
        layout.addWidget(self.stackedWidget, 1109)
        layout.setSpacing(20)

        # Mutual exclusive buttons at the top of window
        btnSD = createToolBtn("Show DIFF", "resource/diff.png")
        btnAS = createToolBtn("Alter Style", "resource/alter.png")
        self.btnSR = createToolBtn("Show Result", "resource/result.png")
        btnFB = createToolBtn("Feedback", "resource/feedback.png")
        btnEX = createToolBtn("Export", "resource/download.png")
        btnEX.setCheckable(False)
        btnEP = createToolBtn("Return Enter", "resource/home.png")
        btnEP.setCheckable(False)
        btnGrp = QButtonGroup(self)
        btnGrp.addButton(btnSD)
        btnGrp.addButton(btnAS)
        btnGrp.addButton(self.btnSR)
        self.btnSR.setChecked(True)
        btnGrp.addButton(btnFB)
        btnGrp.setExclusive(True)
        layoutBtn.addWidget(btnSD, 1)
        layoutBtn.addWidget(btnAS, 1)
        layoutBtn.addWidget(self.btnSR, 1)
        layoutBtn.addWidget(btnFB, 1)
        layoutBtn.addWidget(btnEX, 1)
        layoutBtn.addWidget(btnEP, 1)

        """Show Result"""
        pageSR = QWidget()
        self.stackedWidget.addWidget(pageSR)  # index = 0
        self.layoutSR = QHBoxLayout()
        pageSR.setLayout(self.layoutSR)
        self.figureSR = figure(facecolor="white")
        self.canvasSR = FigureCanvas(self.figureSR)
        self.layoutSR.addWidget(self.canvasSR, 4)

        """Show DIFF"""
        pageSD = QWidget()
        self.stackedWidget.addWidget(pageSD)  # index = 1
        self.layoutSD = QGridLayout()
        pageSD.setLayout(self.layoutSD)
        self.layoutSD.addWidget(createLabPix("resource/beforeFig.png"), 0, 0, 4, 1)
        self.layoutSD.addWidget(createLabPix("resource/afterFig.png"), 0, 1, 4, 1)
        self.layoutSD.addWidget(QLabel("Before Overlap"), 4, 0, 1, 1)
        self.layoutSD.addWidget(QLabel("After Overlap"), 4, 1, 1, 1)

        """Alter Style"""
        pageAS = QWidget()
        self.stackedWidget.addWidget(pageAS)  # index = 2
        layoutAS = QVBoxLayout()
        pageAS.setLayout(layoutAS)
        noticeLabel = QLabel("Please choose one style\n(Images below are for illustration only)")
        layoutAS.addWidget(noticeLabel, 1)
        layoutASB = QHBoxLayout()
        layoutAS.addLayout(layoutASB, 9)
        layoutASCub = QVBoxLayout()
        layoutASCirc = QVBoxLayout()
        layoutASB.addLayout(layoutASCub, 1)
        layoutASB.addLayout(layoutASCirc, 1)

        # Radio buttons to change style
        self.btnASCub = createRadioBtn("Cubes")
        self.btnASCirc = createRadioBtn("Circles")

        layoutASCub.addWidget(createLabPix("resource/cubes.png"), 4)
        layoutASCub.addWidget(self.btnASCub, 1)
        layoutASCirc.addWidget(createLabPix("resource/circles.png"), 4)
        layoutASCirc.addWidget(self.btnASCirc, 1)

        """Feedback"""
        pageFB = QWidget()
        self.stackedWidget.addWidget(pageFB)  # index = 3
        self.layoutFB = QVBoxLayout()
        pageFB.setLayout(self.layoutFB)
        self.webFB = QWebEngineView(self)
        # get HTML from folder questionnaire
        self.webFB.load(QUrl(QFileInfo("questionnaire/questionnaire1.html").absoluteFilePath()))
        self.layoutFB.addWidget(self.webFB, 1)

        """Button Clicked Effects"""
        self.btnSR.clicked.connect(self.click_goSR)
        btnSD.clicked.connect(self.click_goSD)
        btnAS.clicked.connect(self.click_goAS)
        btnFB.clicked.connect(self.click_goFB)
        btnEX.clicked.connect(self.click_goEX)
        btnEP.clicked.connect(self.click_goEP)

        """radioButton Checked Effects"""
        self.btnASCub.toggled.connect(self.set_styleCub)
        self.btnASCirc.toggled.connect(self.set_styleCirc)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """
        Rewrite the resizeEvent of the QWidget to
        help resize the spacing between buttons
        :param a0: QtGui.QResizeEvent: Detect the size change of window
        :return: None
        """
        self.reSizeCanvas()

    """Methods for Change StackedPages"""

    def click_goSR(self):
        """
        Show the result page
        :return: None
        """
        self.stackedWidget.setCurrentIndex(0)

    def click_goSD(self):
        """
        Show the show difference page
        :return: None
        """
        self.stackedWidget.setCurrentIndex(1)

    def click_goAS(self):
        """
        Show the alter style page
        :return: None
        """
        self.stackedWidget.setCurrentIndex(2)

    def click_goFB(self):
        """
        Show the feedback HTML and refresh it every click
        :return: None
        """
        for i in range(self.layoutFB.count()):
            self.layoutFB.itemAt(i).widget().deleteLater()
        self.webFB = QWebEngineView(self)
        self.webFB.load(
            QUrl(QFileInfo("questionnaire/questionnaire1.html").absoluteFilePath()))
        self.layoutFB.addWidget(self.webFB, 1)
        self.stackedWidget.setCurrentIndex(3)

    def click_goEX(self):
        """
        Transform the result figure into png and export to local computer
        :return: None
        """
        fd, fp = QFileDialog.getSaveFileName(
            self.stackedWidget, "save file", "", "*.png;;All Files(*)")
        plt.savefig("overlap.png")
        image = QImage("overlap.png")
        image.save(fd)

    def click_goEP(self):
        """
        Show the enter page and hide result page
        :return: None
        """
        self.sign_toEnter.emit()
        self.hide()

    def method_handle_sign(self):
        """
        Handle the signal from EnterPage.py and load the result figure
        :return: None
        """
        self.btnSR.setChecked(True)
        with open("resource/sample_input.txt", "r", encoding="utf-8") as patternSelect:
            if patternSelect.read(1) == "#":
                # self.patternNum is current overlap style choice
                self.patternNum = 1
                # self.patternChoice, for #, only cub choice
                self.inputChoice = 2
                self.btnASCub.setChecked(True)
                self.btnASCirc.setChecked(False)
            else:
                self.patternNum = 2
                self.inputChoice = 1
                self.btnASCub.setChecked(False)
                self.btnASCirc.setChecked(True)
        self.figureSR = overlapDef.figurePrint(self.patternNum)
        self.refreshCanvas()
        self.stackedWidget.setCurrentIndex(0)
        self.show()

    def set_styleCub(self):
        """
        The def called by alter style page Cubes button,
        change the figure of result and images of show difference page,
        or forbid user from changing style
        :return: None
        """
        if self.btnASCub.isChecked():
            if self.btnASCirc.isChecked() is not True:
                if self.inputChoice == 2:
                    self.patternNum = 1
                    self.figureSR = overlapDef.figurePrint(1)
                elif self.inputChoice == 1:
                    # User can't change the style, forbid it
                    alert = QMessageBox(
                        QMessageBox.Warning, "Warning", "This will violate the code, selection failed")
                    alert.exec_()
        self.refreshCanvas()

    def set_styleCirc(self):
        """
        The def called by alter style page Circles button,
        change the figure of result and images of show difference page
        :return: None
        """
        if self.btnASCub.isChecked() is not True:
            if self.btnASCirc.isChecked():
                # 所有都可以改变为Cub
                self.patternNum = 2
                self.figureSR = overlapDef.figurePrint(2)
        self.refreshCanvas()

    def refreshCanvas(self):
        """
        Refresh the figure of result page and images of show difference page
        :return: None
        """
        # Show DIFF
        for i in range(self.layoutSD.count()):  # delete all QWidgets
            self.layoutSD.itemAt(i).widget().deleteLater()
        self.layoutSD.addWidget(createLabPix("resource/beforeFig.png"), 0, 0, 4, 1)
        self.layoutSD.addWidget(createLabPix("resource/afterFig.png"), 0, 1, 4, 1)
        self.layoutSD.addWidget(QLabel("Before Overlap"), 4, 0, 1, 1)
        self.layoutSD.addWidget(QLabel("After Overlap"), 4, 1, 1, 1)

        # Show Result
        for m in range(self.layoutSR.count()):
            self.layoutSR.itemAt(m).widget().deleteLater()
        self.figureSR = plt.gcf()
        self.canvasSR = FigureCanvas(self.figureSR)
        self.layoutSR.addWidget(self.canvasSR, 4)
        self.canvasSettings()

    def canvasSettings(self):
        """
        Set the basic functions of the canvas of result page
        :return: None
        """
        self.reSizeCanvas()
        self.toolBar = NavigationToolbar(self.canvasSR, self)
        self.toolBar.hide()
        self.canvasSR.mpl_connect('scroll_event', self.zoomEvent)
        self.canvasSR.mpl_connect("button_press_event", self.pan)
        self.canvasSR.mpl_connect("button_release_event", self.onRelease)

    def zoomEvent(self, event):
        """
        Zoom in and zoom out functions
        :param event: cursor actions from user
        :return: None
        """
        self.canvasSR.mpl_disconnect(
            self.canvasSR.mpl_connect("button_press_event", self.pan))

        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        fanwei = (x_max - x_min) / 10

        if event.button == 'up':
            plt.cla()
            axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
            axtemp.set(ylim=(y_min + fanwei, y_max - fanwei))
            zoomRatio = x_max / 6
            graphDemo = Graph()
            # 2 represents pattern 2, NEED automatic checking
            graphDemo.readInput("resource/sample_input.txt", self.patternNum)
            # window range specifies the coordinate settings
            windowRange = calOverlapLayout(graphDemo, self.patternNum)

            if self.patternNum == 1:
                pattern1Draw(graphDemo, axtemp, zoomRatio)
            else:
                pattern2Draw(graphDemo, axtemp, zoomRatio)
            plt.grid(False)
            self.refreshCanvas()

        elif event.button == 'down':
            print('down')
            plt.cla()
            axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
            axtemp.set(ylim=(y_min - fanwei, y_max + fanwei))
            zoomRatio = x_max / 6

            graphDemo = Graph()
            # 2 represents pattern 2, NEED automatic checking
            graphDemo.readInput("resource/sample_input.txt", self.patternNum)
            # window range specifies the coordinate settings
            windowRange = calOverlapLayout(graphDemo, self.patternNum)

            if self.patternNum == 1:
                pattern1Draw(graphDemo, axtemp, zoomRatio)
            else:
                pattern2Draw(graphDemo, axtemp, zoomRatio)
            plt.grid(False)
            self.refreshCanvas()

        self.canvasSR.mpl_connect("button_press_event", self.pan)

    def pan(self, event):
        """
        Drag figure function
        :param event: cursor actions from user
        :return: None
        """
        if event.button == 1:
            self.toolBar = NavigationToolbar(self.canvasSR, self)
            self.toolBar.hide()
            self.toolBar.pan()
        else:
            pass

    def onRelease(self, event):
        """
        Cancel the functions of zoom and drag of the canvas
        :param event: cursor actions from user
        :return: None
        """
        self.canvasSR.mpl_disconnect(self.canvasSR.mpl_connect("button_press_event", self.pan))
        if hasattr(self, '_pan_start'):
            del self._pan_start

    def reSizeCanvas(self):
        """
        Resize the margins of result canvas
        :return: None
        """
        height = self.stackedWidget.height()
        width = self.stackedWidget.width()
        if width > height:
            self.layoutSR.setContentsMargins(
                (width - height) / 2, 0, (width - height) / 2, 0)
        else:
            self.layoutSR.setContentsMargins(
                0, (height - width) / 2, 0, (height - width) / 2)
