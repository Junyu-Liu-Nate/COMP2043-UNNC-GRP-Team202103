# 创建QPushButton的global函数
import PyQt5.Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QPlainTextEdit, QRadioButton, QLabel, QToolButton

# 创建QPushButton并规定大小与格式
def createBtn(str):
    button = QPushButton(str)
    button.setMaximumSize(900, 130)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # setSizePolicy(水平策略, 竖直策略)
    return button

# 创建QRadioButton
def createRadioBtn(str):
    # img = overlapPattern.plt.gcf()  # get current figure
    # canvas = FigureCanvasQtAgg(img)
    # layout.addWidget(canvas)
    button = QRadioButton(str)
    button.setMaximumSize(900, 130)  # 这个后面看情况要调整
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return button

# 创建QToolButton, 记得加图片地址
def createToolBtn(str):
    button = QToolButton()
    button.setText(str)
    button.setMaximumSize(900, 130)  # 看情况调整
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return button

# 创建QPlainTextEdit
def createText(str):
    textEdit = QPlainTextEdit(str)
    textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return textEdit

# 创建QWidget: label承载QPixmap
def createLabPix(str):
    label = QLabel()
    img = QPixmap(str)
    label.setPixmap(img)
    label.setAlignment(Qt.AlignCenter)
    # label.setScaledContents(True)
    img.scaled(600, 600, Qt.KeepAspectRatio)
    # label.setScaledContents(True)
    # label.setFixedSize(600, 600)
    # label.setMinimumSize(700, 700)
    return label