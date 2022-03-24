import sys

from PyQt5.QtWidgets import QApplication

from EnterPage import enterPage
from ResultPage import resultPage



if __name__ == "__main__":
    app = QApplication(sys.argv)

    enter = enterPage()
    result = resultPage()

    enter.sign_toResult.connect(result.method_handle_sign)  # 不要加括号
    result.sign_toEnter.connect(enter.method_handle_sign)

    enter.show()

    # 希望窗口显示位置与大小可以相同

    sys.exit(app.exec_())

