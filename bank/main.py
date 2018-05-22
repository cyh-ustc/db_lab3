
import sys
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QStyleFactory

from mainWindow import mainWindow
from bank import Ui_MainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = mainWindow()
    m.setFixedSize(m.size())
    m.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowCloseButtonHint)
    app.setStyle(QStyleFactory.create("fusion"))
    m.show()

    app.exec()