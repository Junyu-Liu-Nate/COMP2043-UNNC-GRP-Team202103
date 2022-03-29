import sys

from PyQt5.QtWidgets import QApplication

from test import forTest
from receive import RTest

if __name__ == "__main__":
    app = QApplication(sys.argv)

    tt = forTest()
    rr = RTest()
    tt.signalTest.connect(rr.handle_signal)

    tt.show()
    sys.exit(app.exec_())