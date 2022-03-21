import PyQt5
from PyQt5.QtCore import pyqtSignal  # PyQt5.QtCore.Qt.AlignCenter
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QToolButton, QPushButton, QLabel, \
    QFileDialog

from widgetsCreator import createLabPix, createToolBtn, createText, createRadioBtn


class resultPage(QWidget):
    sign_toEnter = pyqtSignal()

    def __init__(self):
        super(resultPage, self).__init__()
        self.resize(1000, 800)
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
        layoutSR = QHBoxLayout()
        pageSR.setLayout(layoutSR)
        # addStretch使图片居中
        layoutSR.addStretch(1)
        layoutSR.addWidget(createLabPix("resource/cubes.png"), 4)  # 直接放进去避免花里胡哨的变量名
        layoutSR.addStretch(1)

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

        layoutASCub.addWidget(createLabPix("resource/cubes.png"), 4)
        layoutASCub.addWidget(createRadioBtn("Cubes"), 1)
        layoutASCirc.addWidget(createLabPix("resource/circles.png"), 4)
        layoutASCirc.addWidget(createRadioBtn("Circles"), 1)

        """Feedback"""
        pageFB = QWidget()
        self.stackedWidget.addWidget(pageFB)  # index = 3
        layoutFB = QVBoxLayout()
        pageFB.setLayout(layoutFB)

        # 随机问卷要不要?
        quesFB1 = QLabel("I'm question 1")
        layoutFB1 = QHBoxLayout()
        ansFBRadio1 = createRadioBtn("I'm answer 1")
        ansFBRadio2 = createRadioBtn("I'm answer 2")
        ansFBRadio3 = createText("Other answer ...")
        layoutFB1.addWidget(ansFBRadio1, 1)
        layoutFB1.addWidget(ansFBRadio2, 1)
        layoutFB1.addWidget(ansFBRadio3, 2)
        layoutFB.addWidget(quesFB1, 1)
        layoutFB.addLayout(layoutFB1, 1)

        quesFB2 = QLabel("I'm question 2")
        ansFB2 = createText("Write your answer here")
        layoutFB.addWidget(quesFB2, 1)
        layoutFB.addWidget(ansFB2, 2)

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
        image = QImage("resource/cubes.png")
        image.save(fd)

    def click_goEP(self):
        self.sign_toEnter.emit()  # 发射信号, 返回Enter Page, 别打错字了
        self.hide()

    def method_handle_sign(self):
        self.show()