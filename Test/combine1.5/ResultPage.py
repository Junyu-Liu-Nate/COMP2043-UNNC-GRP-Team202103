import PyQt5
import PyQt5.Qt
from PyQt5 import Qt, QtGui, QtCore
# PyQt5.QtCore.Qt.AlignCenter
from PyQt5.QtCore import pyqtSignal, QUrl, QFileInfo, QMutex
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QLabel, QFileDialog, QSplitter, \
    QButtonGroup, QMessageBox, QApplication
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import overlapDef
from overlap.graph import Graph
from overlap.layoutAlgorithmOverlap import calOverlapLayout
from overlap.overlapPatten import pattern1Draw, pattern2Draw
from widgetsCreator import createLabPix, createToolBtn, createText, createRadioBtn, createBtn
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from overlap.layoutAlgorithmOriginal import calLayout


class resultPage(QWidget):

    sign_toEnter = pyqtSignal()
    sign_showFigure = pyqtSignal()
    ans1Text = "no button"
    qmutx = QMutex()  # 线程锁

    def __init__(self):
        super(resultPage, self).__init__()
        self.patternNum = None
        desktop = QApplication.desktop()
        width = desktop.width()
        height = desktop.height()
        self.resize(int(width/1.5), int(height/1.5))
        self.setWindowTitle("OVERLAP")

        pixIcon = PyQt5.QtGui.QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)  # icon for Result Page
        self.setWindowIcon(iconEP)

        with open("resource/styleSettings.txt", "r") as self.style:
            textOfStyle = self.style.read()
            self.setStyleSheet(textOfStyle)
            self.style.close()

        self.initUI()

    def calculateLayout(self, patternNum):
        graphDemo = Graph()
        graphDemo.readInput("resource/sample_input.txt", patternNum)

        # Calculate the original layout
        calLayout(graphDemo)
        f, (ax1) = plt.subplots(1, 1, figsize=(10, 9))
        f.subplots_adjust(hspace=0, wspace=0)

        if patternNum == 1:
            pattern1Draw(graphDemo, ax1, 1)
        else:
            pattern2Draw(graphDemo, ax1, 1)

        plt.grid(False)
        ax1.set_xlim(-6, 6)
        ax1.set_ylim(-6, 6)

        plt.savefig("resource/beforeFig.png")

        # Calculate the layout after overlapping
        windowRange = calOverlapLayout(graphDemo, patternNum)
        zoomRatio = windowRange[1] / 6
        if zoomRatio == 0:
            zoomRatio = 1

        # ----- Draw Overlapped Layout Graph -----#
        # Specify the size of figure window
        f, (ax2) = plt.subplots(1, 1, figsize=(10, 9))
        f.subplots_adjust(hspace=0, wspace=0)

        if patternNum == 1:
            pattern1Draw(graphDemo, ax1, zoomRatio)
        else:
            pattern2Draw(graphDemo, ax1, zoomRatio)

        plt.grid(False)
        ax2.set_xlim(windowRange[0], windowRange[1])
        ax2.set_ylim(windowRange[0], windowRange[1])

        plt.savefig("resource/afterFig.png")

    def initUI(self):
        # 整个Widget的layout
        layout = QVBoxLayout()
        self.setLayout(layout)  # 别忘了, 否则不显示
        layoutBtn = QHBoxLayout()
        self.stackedWidget = QStackedWidget()
        # 做一个分割线
        splitter = QSplitter(QtCore.Qt.Horizontal)
        layout.addLayout(layoutBtn, 150)
        layout.addWidget(splitter, 2)
        layout.addWidget(self.stackedWidget, 1109)
        layout.setSpacing(20)

        # 最上方的按钮们
        btnSD = createToolBtn("Show DIFF", "resource/diff.png")
        btnAS = createToolBtn("Alter Style", "resource/alter.png")
        self.btnSR = createToolBtn("Show Result", "resource/result.png")
        btnFB = createToolBtn("Feedback", "resource/feedback.png")
        btnEX = createToolBtn("Export", "resource/download.png")
        btnEX.setCheckable(False)  # 不检查选中
        btnEP = createToolBtn("Return Enter", "resource/home.png")
        btnEP.setCheckable(False)
        btnGrp = QButtonGroup(self)  # 这个self不能少
        btnGrp.addButton(btnSD)
        btnGrp.addButton(btnAS)
        btnGrp.addButton(self.btnSR)
        self.btnSR.setChecked(True)  # 最开始这个就是开启的
        btnGrp.addButton(btnFB)
        btnGrp.setExclusive(True)  # 设置按扭间checked状态互斥
        layoutBtn.addWidget(btnSD, 1)
        layoutBtn.addWidget(btnAS, 1)
        layoutBtn.addWidget(self.btnSR, 1)
        layoutBtn.addWidget(btnFB, 1)
        layoutBtn.addWidget(btnEX, 1)
        layoutBtn.addWidget(btnEP, 1)

        # 一个个的Widget做
        """Show Result"""
        pageSR = QWidget()
        self.stackedWidget.addWidget(pageSR)  # index = 0
        self.layoutSR = QHBoxLayout()
        pageSR.setLayout(self.layoutSR)
        # addStretch使图片居中
        # layoutSR.addStretch(1)
        # layoutSR.addWidget(createLabPix("resource/cubes.png"), 4)  # 直接放进去避免花里胡哨的变量名
        # layoutSR.addStretch(1)
        self.figureSR = figure(facecolor="white")  # 这个必须在后面才开始
        self.canvasSR = FigureCanvas(self.figureSR)  # 可能缺少参数
        self.layoutSR.addWidget(self.canvasSR, 4)

        """Show DIFF"""
        pageSD = QWidget()
        self.stackedWidget.addWidget(pageSD)  # index = 1
        self.layoutSD = QHBoxLayout()
        pageSD.setLayout(self.layoutSD)
        self.layoutSDBef = QVBoxLayout()
        self.layoutSDAf = QVBoxLayout()
        self.layoutSD.addLayout(self.layoutSDBef, 1)
        self.layoutSD.addLayout(self.layoutSDAf, 1)

        pixBefore = createLabPix("resource/beforeFig.png")
        self.layoutSDBef.addWidget(pixBefore, 4)
        self.layoutSDBef.addWidget(QLabel("Before"), 1)
        self.pixAfter = createLabPix("resource/afterFig.png")
        self.layoutSDAf.addWidget(self.pixAfter, 4)
        self.layoutSDAf.addWidget(QLabel("After"), 1)

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

        # 这里并没有给具体的checked
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
        self.webFB.load(
            QUrl(QFileInfo("questionnaire/questionnaire1.html").absoluteFilePath()))
        self.layoutFB.addWidget(self.webFB, 1)
        # webFB.load(QUrl(r"https://forms.office.com/r/BQXHH6FS1Z"))


        """Export"""
        # 这只是一个按钮, 点击之后可以将图片保存到本地

        """Return Home"""
        # 这只是一个按钮，点击之后可以返回Enter Page

        """Button Clicked Effects"""
        self.btnSR.clicked.connect(self.click_goSR)  # 不要加括号
        btnSD.clicked.connect(self.click_goSD)
        btnAS.clicked.connect(self.click_goAS)
        btnFB.clicked.connect(self.click_goFB)
        btnEX.clicked.connect(self.click_goEX)
        btnEP.clicked.connect(self.click_goEP)
        # btnFBover.clicked.connect(self.click_submit)

        """radioButton Checked Effects"""
        self.btnASCub.toggled.connect(self.set_styleCub)
        self.btnASCirc.toggled.connect(self.set_styleCirc)

    # 重写窗口resizeEvent
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.reSizeCanvas()

    """Methods for Change StackedPages"""

    def click_goSR(self):
        self.stackedWidget.setCurrentIndex(0)

    def click_goSD(self):
        self.stackedWidget.setCurrentIndex(1)

    def click_goAS(self):
        self.stackedWidget.setCurrentIndex(2)

    def click_goFB(self):
        for i in range(self.layoutFB.count()):  # 用这个把layoutSR中的控件删干净
            self.layoutFB.itemAt(i).widget().deleteLater()
        self.webFB = QWebEngineView(self)
        self.webFB.load(
            QUrl(QFileInfo("questionnaire/questionnaire1.html").absoluteFilePath()))
        self.layoutFB.addWidget(self.webFB, 1)
        self.stackedWidget.setCurrentIndex(3)

    def click_goEX(self):
        # 保存到本地
        fd, fp = QFileDialog.getSaveFileName(
            self.stackedWidget, "save file", "", "*.png;;All Files(*)")
        plt.savefig("overlap.png")
        image = QImage("overlap.png")
        image.save(fd)

    def click_goEP(self):
        self.sign_toEnter.emit()  # 发射信号, 返回Enter Page, 别打错字了
        self.hide()

    def method_handle_sign(self):
        print("handle")
        self.stackedWidget.setCurrentIndex(0)
        self.btnSR.setChecked(True)
        # sample_input被传进来的时候就进行一次判断
        with open("resource/sample_input.txt", "r", encoding="utf-8") as patternSelect:
            if(patternSelect.read(1) == "#"):
                # self.patternNum is current overlap style choice
                self.patternNum = 1
                # self.patternChoice, for #, only cub choice
                self.inputChoice = 2
                # 这两个干脆只要一个函数好了, 判断哪个被checked
                self.btnASCub.setChecked(True)
                self.btnASCirc.setChecked(False)
            else:
                self.patternNum = 2
                self.inputChoice = 1
                self.btnASCub.setChecked(False)
                self.btnASCirc.setChecked(True)
        self.figureSR = overlapDef.figurePrint(self.patternNum)
        self.refreshCanvas()
        self.show()

    def set_styleCub(self):
        print("set Style")
        # 选择Cub按钮, 想要改变为Cub
        if self.btnASCub.isChecked():
            if self.btnASCirc.isChecked() is not True:
                # 如果是有两种选择的input
                if self.inputChoice == 2:
                    self.patternNum = 1
                    self.figureSR = overlapDef.figurePrint(1)
                elif self.inputChoice == 1:
                    # 不允许改变
                    alert = QMessageBox(
                        QMessageBox.Warning, "Warning", "This will violate the code, selection failed")
                    alert.exec_()
        self.refreshCanvas()
    def set_styleCirc(self):
        # 选择Circ按钮, 想要改变为Circ
        if self.btnASCub.isChecked() is not True:
            if self.btnASCirc.isChecked():
                # 所有都可以改变为Cub
                self.patternNum = 2
                self.figureSR = overlapDef.figurePrint(2)
        # 更新画布
        self.refreshCanvas()

    def refreshCanvas(self):
        print("refresh Canvas")
        # 设置Show DIFF
        for i in range(self.layoutSDBef.count()):
            self.layoutSDBef.itemAt(i).widget().deleteLater()
        self.layoutSDBef.addWidget(createLabPix("resource/beforeFig.png"), 4)
        self.layoutSDBef.addWidget(QLabel("Before"), 1)
        for j in range(self.layoutSDAf.count()):  # 用这个把layoutSR中的控件删干净
            self.layoutSDAf.itemAt(j).widget().deleteLater()
        self.layoutSDAf.addWidget(createLabPix("resource/afterFig.png"), 4)
        self.layoutSDAf.addWidget(QLabel("After"), 1)

        # 设置Show Result
        for m in range(self.layoutSR.count()):  # 用这个把layoutSR中的控件删干净
            self.layoutSR.itemAt(m).widget().deleteLater()
        self.figureSR = plt.gcf()
        self.canvasSR = FigureCanvas(self.figureSR)
        self.layoutSR.addWidget(self.canvasSR, 4)
        print("after refresh, before set Canvas")
        self.canvasSettings()

    def canvasSettings(self):
        print("set Canvas")
        self.reSizeCanvas()
        self.toolBar = NavigationToolbar(self.canvasSR, self)
        self.toolBar.hide()
        self.canvasSR.mpl_connect('scroll_event', self.zoomEvent)
        self.canvasSR.mpl_connect("button_press_event", self.pan)
        self.canvasSR.mpl_connect("button_release_event", self.onRelease)
        print("finish canvasSetting")

    def zoomEvent(self, event):
        print("zoom event")
        self.canvasSR.mpl_disconnect(
            self.canvasSR.mpl_connect("button_press_event", self.pan))

        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        fanwei = (x_max - x_min) / 10

        print("hi")
        if event.button == 'up':
            print("up")
            plt.cla()
            # self.canvasSR.mpl_disconnect(self.idBtnPress)
            axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
            axtemp.set(ylim=(y_min + fanwei, y_max - fanwei))
            zoomRatio = x_max / 6
            graphDemo = Graph()
            # 2 represents pattern 2, NEED automatic checking!!!
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
            # 2 represents pattern 2, NEED aumatic checking!!!
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
        print("pan")
        if event.button == 1:
            self.toolBar = NavigationToolbar(self.canvasSR, self)
            self.toolBar.hide()
            self.toolBar.pan()
        else:
            pass

    def onRelease(self, event):
        print("release")
        self.canvasSR.mpl_disconnect(self.canvasSR.mpl_connect("button_press_event", self.pan))
        if hasattr(self, '_pan_start'):
            del self._pan_start

    def reSizeCanvas(self):
        height = self.stackedWidget.height()
        width = self.stackedWidget.width()
        if width > height:
            self.layoutSR.setContentsMargins(
                (width - height) / 2, 0, (width - height) / 2, 0)
        else:
            self.layoutSR.setContentsMargins(
                0, (height - width) / 2, 0, (height - width) / 2)
