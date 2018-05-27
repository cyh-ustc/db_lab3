# -*- coding: utf-8 -*-
import sys
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMessageBox

from mainWindow import mainWindow
from bank import Ui_MainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('fusion'))
    m = mainWindow()
    z = m.connectDB()
    while z == QMessageBox.Retry:
        z = m.connectDB()
    if z == QMessageBox.Abort:
        exit()
    m.init()
    m.setFixedSize(m.size())
    m.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

    m.show()
    app.exec()