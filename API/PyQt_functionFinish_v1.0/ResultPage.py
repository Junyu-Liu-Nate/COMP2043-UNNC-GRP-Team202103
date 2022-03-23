import PyQt5
from PyQt5.QtCore import pyqtSignal  # PyQt5.QtCore.Qt.AlignCenter
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QToolButton, QPushButton, QLabel, QFileDialog
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import overlapDef
from widgetsCreator import createLabPix, createToolBtn, createText, createRadioBtn, createBtn
import globalVariable as glv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

# ans1Text = "no button"

class resultPage(QWidget):
    sign_toEnter = pyqtSignal()
    sign_showFigure = pyqtSignal()
    ans1Text = "no button"

    def __init__(self):
        super(resultPage, self).__init__()
        self.resize(1600, 1000)
        self.setWindowTitle("OVERLAP")

        pixIcon = PyQt5.QtGui.QPixmap("resource/icon.png")
        iconEP = QIcon(pixIcon)  # icon for Result Page
        self.setWindowIcon(iconEP)

        self.initUI()

    def initUI(self):
        # 整个Widget的layout
        layout = QVBoxLayout()
        self.setLayout(layout)  # 别忘了, 否则不显示
        layoutBtn = QHBoxLayout()
        self.stackedWidget = QStackedWidget()
        layout.addLayout(layoutBtn, 1)
        layout.addWidget(self.stackedWidget, 1)
        layout.setSpacing(20)

        # 最上方的按钮们
        btnSD = createToolBtn("Show DIFF")
        btnAS = createToolBtn("Alter Style")
        btnSR = createToolBtn("Show Result")
        btnFB = createToolBtn("Feedback")
        btnEX = createToolBtn("Export")
        btnEP = createToolBtn("Return Enter")
        layoutBtn.addWidget(btnSD, 1)
        layoutBtn.addWidget(btnAS, 1)
        layoutBtn.addWidget(btnSR, 1)
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
        self.canvasSR = FigureCanvas()
        self.layoutSR.addWidget(self.canvasSR, 4)

        """Show DIFF"""
        pageSD = QWidget()
        self.stackedWidget.addWidget(pageSD)  # index = 1
        layoutSD = QHBoxLayout()
        pageSD.setLayout(layoutSD)
        layoutSDBef = QVBoxLayout()
        layoutSDAf = QVBoxLayout()
        layoutSD.addLayout(layoutSDBef, 1)
        layoutSD.addLayout(layoutSDAf, 1)

        layoutSDBef.addWidget(createLabPix("resource/cubes.png"), 4)
        layoutSDBef.addWidget(QLabel("Before"), 1)
        layoutSDAf.addWidget(createLabPix("resource/circles.png"), 4)
        layoutSDAf.addWidget(QLabel("After"), 1)

        """Alter Style"""
        pageAS = QWidget()
        self.stackedWidget.addWidget(pageAS)  # index = 2
        layoutAS = QHBoxLayout()
        pageAS.setLayout(layoutAS)
        layoutASCub = QVBoxLayout()
        layoutASCirc = QVBoxLayout()
        layoutAS.addLayout(layoutASCub, 1)
        layoutAS.addLayout(layoutASCirc, 1)

        self.btnASCub = createRadioBtn("Cubes")
        self.btnASCirc = createRadioBtn("Circles")

        layoutASCub.addWidget(createLabPix("resource/cubes.png"), 4)
        layoutASCub.addWidget(self.btnASCub, 1)
        layoutASCirc.addWidget(createLabPix("resource/circles.png"), 4)
        layoutASCirc.addWidget(self.btnASCirc, 1)

        """Feedback"""
        pageFB = QWidget()
        self.stackedWidget.addWidget(pageFB)  # index = 3
        layoutFB = QVBoxLayout()
        pageFB.setLayout(layoutFB)

        # 随机问卷要不要?
        quesFB1 = QLabel("I'm question 1")
        layoutFB1 = QHBoxLayout()
        self.ansFBRadio1 = createRadioBtn("I'm answer 1")
        self.ansFBRadio2 = createRadioBtn("I'm answer 2")
        self.ansFBRadio3 = createText("Other answer ...")
        layoutFB1.addWidget(self.ansFBRadio1, 1)
        layoutFB1.addWidget(self.ansFBRadio2, 1)
        layoutFB1.addWidget(self.ansFBRadio3, 2)
        layoutFB.addWidget(quesFB1, 1)
        layoutFB.addLayout(layoutFB1, 1)

        self.quesFB2 = QLabel("I'm question 2")
        self.ansFB2 = createText("Write your answer here")
        layoutFB.addWidget(self.quesFB2, 1)
        layoutFB.addWidget(self.ansFB2, 2)

        btnFBover = createBtn("Submit")
        layoutFB.addWidget(btnFBover, 1)

        """Export"""
        # 这只是一个按钮, 点击之后可以将图片保存到本地

        """Return Home"""
        # 这只是一个按钮，点击之后可以返回Enter Page

        """Button Clicked Effects"""
        btnSR.clicked.connect(self.click_goSR)  # 不要加括号
        btnSD.clicked.connect(self.click_goSD)
        btnAS.clicked.connect(self.click_goAS)
        btnFB.clicked.connect(self.click_goFB)
        btnEX.clicked.connect(self.click_goEX)
        btnEP.clicked.connect(self.click_goEP)
        btnFBover.clicked.connect(self.click_submit)

        """radioButton Checked Effects"""
        self.btnASCub.toggled.connect(self.set_globalCub)
        self.btnASCirc.toggled.connect(self.set_globalCirc)

        self.ansFBRadio1.toggled.connect(lambda: self.writeBtnFB(self.ansFBRadio1.text()))
        self.ansFBRadio2.toggled.connect(lambda: self.writeBtnFB(self.ansFBRadio2.text()))


    """Methods for Change StackedPages"""
    def click_goSR(self):
        self.stackedWidget.setCurrentIndex(0)

    def click_goSD(self):
        self.stackedWidget.setCurrentIndex(1)

    def click_goAS(self):
        self.stackedWidget.setCurrentIndex(2)

    def click_goFB(self):
        self.stackedWidget.setCurrentIndex(3)

    def click_goEX(self):
        # 保存到本地
        fd, fp = QFileDialog.getSaveFileName(self.stackedWidget, "save file", "", "*.png;;All Files(*)")
        # image = QImage("resource/cubes.png")
        plt.savefig("overlap.png")
        image = QImage("overlap.png")
        image.save(fd)

    def click_goEP(self):
        self.sign_toEnter.emit()  # 发射信号, 返回Enter Page, 别打错字了
        self.hide()

    def set_globalCub(self):
        if self.btnASCub.isChecked():
            glv.set("cub", "true")
            glv.set("circ", "false")
        else:
            glv.set("cub", "false")
            glv.set("circ", "true")
        self.changeFigure()

    def set_globalCirc(self):
        if self.btnASCirc.isChecked():
            glv.set("circ", "true")
            glv.set("cub", "false")
        else:
            glv.set("circ", "false")
            glv.set("cub", "true")
        self.changeFigure()

    def writeBtnFB(self, str):
        global ans1Text
        ans1Text = str

    def click_submit(self):
        with open("feedback.txt", "w") as self.f:
            if ans1Text is not None:
                self.f.write(ans1Text)
            self.f.write("\n")  # 换行
            self.f.write(self.ansFBRadio3.toPlainText())
            self.f.write("\n")
            self.f.write(self.ansFB2.toPlainText())
            self.f.close()

    def method_handle_sign(self):
        # self.canvasSR = FigureCanvas(plt.gcf())
        # self.layoutSR.addWidget(self.canvasSR)
        """
        self.layoutSR.addWidget(plt.gcf().canvas)  # 为什么上面那个不能pan...应该是canvas不同之类的问题吧
        """
        # self.toolBar = NavigationToolbar(self.canvasSR, self)
        # self.canvasSR.mpl_connect("button_press_event", self.pan)
        # self.canvasSR.mpl_connect("button_release_event", self.onRelease)
        if glv.get("cub") == "true":
            if glv.get("circ") == "false":
                self.btnASCub.setChecked(True)
        if glv.get("circ") == "true":
            if glv.get("cub") == "false":
                self.btnASCub.setChecked(True)
        self.changeFigure()
        self.show()

    def changeFigure(self):
        for i in range(self.layoutSR.count()):  # 用这个把layoutSR中的控件删干净
            self.layoutSR.itemAt(i).widget().deleteLater()
        if glv.get("cub") == "true":
            if glv.get("circ") == "false":
                self.figureSR = overlapDef.figureCub()
                self.canvasSR = FigureCanvas(self.figureSR)
                self.layoutSR.addWidget(self.canvasSR, 4)
        if glv.get("circ") == "true":
            if glv.get("cub") == "false":
                self.figureSR = overlapDef.figureCirc()
                self.canvasSR = FigureCanvas(self.figureSR)
                self.layoutSR.addWidget(self.canvasSR, 4)
        self.canvasSettings()

    def canvasSettings(self):
        self.toolBar = NavigationToolbar(self.canvasSR, self)
        self.toolBar.hide()
        self.canvasSR.mpl_connect('scroll_event', lambda event: self.zoomEvent(event, self.canvasSR))
        self.canvasSR.mpl_connect("button_press_event", self.pan)
        self.canvasSR.mpl_connect("button_release_event", lambda event: self.onRelease(event, self.canvasSR))

    def zoomEvent(self, event, canvas):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        fanwei = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
            axtemp.set(ylim=(y_min + fanwei, y_max - fanwei))
            # print('up')
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
            axtemp.set(ylim=(y_min - fanwei, y_max + fanwei))
            # print('down')
        canvas.draw_idle()

    def pan(self, event):
        print("pan")
        self.toolBar.pan()

    def onRelease(self, event, canvas):
        print("release")
        canvas.mpl_disconnect(canvas.mpl_connect("button_press_event", self.pan))

    # def pan(self, event):
    #     self.toolBar.pan()
    #
    # def onRelease(self, event):
    #     self.canvasSR.mpl_disconnect(self.canvasSR.mpl_connect("button_press_event", self.pan))