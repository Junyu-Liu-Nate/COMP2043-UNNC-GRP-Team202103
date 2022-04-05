from PyQt5.QtCore import Qt, QUrl, QFileInfo
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QRadioButton, QLabel, QToolButton


def createBtn(str):
    """
    Create QPushButton and restrict its size
    :param str: text of button
    :return: created push button
    """
    button = QPushButton(str)
    button.setMaximumSize(900, 150)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # setSizePolicy(水平策略, 竖直策略)
    return button


def createRadioBtn(str):
    """
    Create QRadioButton and restrict its size
    :param str: text of button
    :return: created radio button
    """
    button = QRadioButton(str)
    button.setMaximumSize(900, 130)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return button


def createToolBtn(str, imgPath):
    """
    Create QToolButton, add icons and restrict its size
    :param str: text of button
    :param imgPath: path of icon image
    :return: created tool button
    """
    button = QToolButton()
    button.setText(str)
    button.setMaximumSize(900, 130)
    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    pixM = QPixmap()
    pixM.load(imgPath)
    icon = QIcon(pixM)
    button.setIcon(icon)
    # text under icon
    button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    button.setCheckable(True)
    return button


def createLabPix(str):
    """
    Create QLabel to display image
    :param str: path of image
    :return: created label
    """
    label = QLabel()
    img = QPixmap(str)
    label.setPixmap(img)
    label.setAlignment(Qt.AlignCenter)
    img.scaled(600, 600, Qt.KeepAspectRatio)
    return label


def createHTML150():
    """
    Create QWebEngineView to display HTML information
    :return: HTML with js effects
    """
    browser = QWebEngineView()
    browser.load(QUrl(QFileInfo("canvas-nest.js/index150.html").absoluteFilePath()))
    return browser


def createHTML200():
    """
    Create QWebEngineView to display HTML information
    :return: HTML with js effects
    """
    browser = QWebEngineView()
    browser.load(QUrl(QFileInfo("canvas-nest.js/index200.html").absoluteFilePath()))
    return browser


def createHTML25():
    """
    Create QWebEngineView to display HTML information
    :return: HTML with js effects
    """
    browser = QWebEngineView()
    browser.load(QUrl(QFileInfo("canvas-nest.js/index25.html").absoluteFilePath()))
    return browser