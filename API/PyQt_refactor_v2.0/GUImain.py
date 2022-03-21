import sys

from PyQt5.QtWidgets import QApplication

from EnterPage import enterPage
from ResultPage import resultPage
from ShowFigure import showFigure

if __name__ == "__main__":
    app = QApplication(sys.argv)

    enter = enterPage()
    result = resultPage()
    show = showFigure()

    enter.sign_toResult.connect(result.method_handle_sign)  # 不要加括号
    result.sign_toEnter.connect(enter.method_handle_sign)
    enter.sign_showFigure.connect(show.method_handle_sign)  # 展示大图, 不要找错爹了...

    enter.show()

    sys.exit(app.exec_())