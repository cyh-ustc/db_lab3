from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex


from bank import Ui_MainWindow
import pymysql

from enum import Enum


branchInfo = ['支行号', '支行名', '城市', '资产']
branchWidth = [0.15, 0.5 ,0.15, 0.15]
branchSearchPre = [' = \'', ' <> \'', ' like \'%']
branchSearchPost = ['\'', '\'', '%\'']
branchSearchIn = ['>', '>=', '=', '<=', '<', '<>']

class branchState(Enum):
    notchosen = 0
    chosen = 1
    edit = 2
    add = 3





class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectDB()


        self.branchSearchCondition = '1'

        self.showBranchs()
        self.connectSignals()
        self.bState = branchState.notchosen



    def connectSignals(self):


        #branch
        self.ui.branchTableView.clicked.connect(self.chooseBranch)
        self.ui.editBranchPushButton.clicked.connect(self.editBranch)
        self.ui.abortBranchPushButton.clicked.connect(self.abortBranch)
        self.ui.deleteBranchPushButton.clicked.connect(self.deleteBranch)
        self.ui.saveBranchPushButton.clicked.connect(self.saveBranch)
        self.ui.addBranchPushButton.clicked.connect(self.addBranch)
        self.ui.branchSearchAssetCheckBox.stateChanged.connect(self.branchSearchConditionChanged)
        self.ui.branchSearchBranchIDCheckBox.stateChanged.connect(self.branchSearchConditionChanged)
        self.ui.branchSearchBranchNameCheckBox.stateChanged.connect(self.branchSearchConditionChanged)
        self.ui.branchSearchCityCheckBox.stateChanged.connect(self.branchSearchConditionChanged)
        self.ui.branchSearchPushButton.clicked.connect(self.updateSearchCondition)
        #branch




#branch
    def branchSearchConditionChanged(self):
        if self.ui.branchSearchAssetCheckBox.isChecked():
            self.ui.branchSearchAssetComboBox.setEnabled(True)
            self.ui.branchSearchAssetLineEdit.setEnabled(True)
        else:
            self.ui.branchSearchAssetComboBox.setEnabled(False)
            self.ui.branchSearchAssetLineEdit.setEnabled(False)

        if self.ui.branchSearchBranchIDCheckBox.isChecked():
            self.ui.branchSearchBranchIDComboBox.setEnabled(True)
            self.ui.branchSearchBranchIDLineEdit.setEnabled(True)
        else:
            self.ui.branchSearchBranchIDComboBox.setEnabled(False)
            self.ui.branchSearchBranchIDLineEdit.setEnabled(False)

        if self.ui.branchSearchCityCheckBox.isChecked():
            self.ui.branchSearchCityComboBox.setEnabled(True)
            self.ui.branchSearchCityLineEdit.setEnabled(True)
        else:
            self.ui.branchSearchCityComboBox.setEnabled(False)
            self.ui.branchSearchCityLineEdit.setEnabled(False)

        if self.ui.branchSearchBranchNameCheckBox.isChecked():
            self.ui.branchSearchBranchNameComboBox.setEnabled(True)
            self.ui.branchSearchBranchNameLineEdit.setEnabled(True)
        else:
            self.ui.branchSearchBranchNameComboBox.setEnabled(False)
            self.ui.branchSearchBranchNameLineEdit.setEnabled(False)

    def connectDB(self):
        self.db = pymysql.connect('localhost', 'root', '135565', 'bank')
        self.dbcursor = self.db.cursor()

    def updateSearchCondition(self):
        if self.ui.branchSearchRangeComboBox.currentIndex() == 0:
            self.branchSearchCondition = '1'
        if self.ui.branchSearchBranchIDCheckBox.isChecked():
            idx = self.ui.branchSearchBranchIDComboBox.currentIndex()
            self.branchSearchCondition += ' and BranchID' + branchSearchPre[idx] + self.ui.branchSearchBranchIDLineEdit.text() + branchSearchPost[idx]
        if self.ui.branchSearchBranchNameCheckBox.isChecked():
            idx = self.ui.branchSearchBranchNameComboBox.currentIndex()
            self.branchSearchCondition += ' and BranchName' + branchSearchPre[idx] + self.ui.branchSearchBranchNameLineEdit.text() + branchSearchPost[idx]
        if self.ui.branchSearchCityCheckBox.isChecked():
            idx = self.ui.branchSearchCityComboBox.currentIndex()
            self.branchSearchCondition += ' and City' + branchSearchPre[idx] + self.ui.branchSearchCityLineEdit.text() + branchSearchPost[idx]
        if self.ui.branchSearchAssetCheckBox.isChecked():
            idx = self.ui.branchSearchAssetComboBox.currentIndex()
            if not self.ui.branchSearchAssetLineEdit.text():
                self.ui.branchSearchAssetLineEdit.setText('0')
            self.branchSearchCondition += ' and Property' + branchSearchIn[idx] + self.ui.branchSearchAssetLineEdit.text()
        print(self.branchSearchCondition)
        self.showBranchs()






    def showBranchs(self):
        self.dbcursor.execute('select * from Branch where %s;'%self.branchSearchCondition)
        results = self.dbcursor.fetchall()
        #self.ui.branchTableView
        self.model = QStandardItemModel(self.ui.branchTableView)
        self.model.setRowCount(len(results))
        self.model.setColumnCount(4)
        for i in range(4):
            self.model.setHeaderData(i, Qt.Horizontal, branchInfo[i])
        self.ui.branchTableView.setModel(self.model)
        for i in range(4):
            w = self.ui.branchTableView.width()
            self.ui.branchTableView.setColumnWidth(i, int(w * branchWidth[i]))
        for i in range(len(results)):
            for j in range(4):
                self.model.setItem(i, j, QStandardItem(str(results[i][j])))
        for i in range(len(results)):
            self.model.item(i, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.ui.branchTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def chooseBranch(self):
        i = self.ui.branchTableView.currentIndex()
        if i.row() != -1:
            idx = self.model.index(i.row(), 0)
            self.ui.branchIDLineEdit.setText(self.model.data(idx))
            idx = self.model.index(i.row(), 1)
            self.ui.branchNameLineEdit.setText(self.model.data(idx))
            idx = self.model.index(i.row(), 2)
            self.ui.branchCityLineEdit.setText(self.model.data(idx))
            idx = self.model.index(i.row(), 3)
            self.ui.branchAsertLineEdit.setText(self.model.data(idx))

            self.bState = branchState.chosen
            self.ui.branchTableView.setEnabled(True)
            self.ui.addBranchPushButton.setEnabled(True)
            self.ui.editBranchPushButton.setEnabled(True)
            self.ui.deleteBranchPushButton.setEnabled(True)
        else:
            self.ui.branchIDLineEdit.setText('')
            self.ui.branchNameLineEdit.setText('')
            self.ui.branchCityLineEdit.setText('')
            self.ui.branchAsertLineEdit.setText('')
            self.bState = branchState.notchosen
            self.ui.branchTableView.setEnabled(True)
            self.ui.branchIDLineEdit.setEnabled(False)
            self.ui.branchNameLineEdit.setEnabled(False)
            self.ui.branchCityLineEdit.setEnabled(False)
            self.ui.branchAsertLineEdit.setEnabled(False)

    def editBranch(self):
        if self.bState == branchState.chosen:
            self.bState = branchState.edit
            self.ui.branchTableView.setEnabled(False)
            self.ui.addBranchPushButton.setEnabled(False)
            self.ui.editBranchPushButton.setEnabled(False)
            self.ui.deleteBranchPushButton.setEnabled(False)
            self.ui.branchIDLineEdit.setEnabled(False)
            self.ui.branchNameLineEdit.setEnabled(True)
            self.ui.branchCityLineEdit.setEnabled(True)
            self.ui.branchAsertLineEdit.setEnabled(True)

    def abortBranch(self):
        if self.bState == branchState.edit:
            self.bState = branchState.chosen
            self.chooseBranch()
        elif self.bState == branchState.add:
            self.bState = branchState.notchosen
            self.ui.branchIDLineEdit.setText('')
            self.ui.branchNameLineEdit.setText('')
            self.ui.branchCityLineEdit.setText('')
            self.ui.branchAsertLineEdit.setText('')

        self.ui.branchTableView.setEnabled(True)
        self.ui.addBranchPushButton.setEnabled(True)
        self.ui.editBranchPushButton.setEnabled(True)
        self.ui.deleteBranchPushButton.setEnabled(True)
        self.ui.branchIDLineEdit.setEnabled(False)
        self.ui.branchNameLineEdit.setEnabled(False)
        self.ui.branchCityLineEdit.setEnabled(False)
        self.ui.branchAsertLineEdit.setEnabled(False)

    def addBranch(self):
        if self.bState == branchState.chosen or self.bState == branchState.notchosen:
            self.bState = branchState.add
            self.ui.branchIDLineEdit.setText('')
            self.ui.branchNameLineEdit.setText('')
            self.ui.branchCityLineEdit.setText('')
            self.ui.branchAsertLineEdit.setText('')
            self.ui.branchIDLineEdit.setEnabled(True)
            self.ui.branchNameLineEdit.setEnabled(True)
            self.ui.branchCityLineEdit.setEnabled(True)
            self.ui.branchAsertLineEdit.setEnabled(True)

    def deleteBranch(self):
        if self.bState == branchState.chosen:
            q = QMessageBox.question(self, '删除一条记录', '确认删除这条记录吗？', QMessageBox.Yes, QMessageBox.No)
            if q == QMessageBox.Yes:
                try:
                    s = "delete from Branch where BranchID = '%s'"%self.ui.branchIDLineEdit.text()
                    self.dbcursor.execute(s)
                    self.db.commit()

                except Exception as e:
                    self.db.rollback()
                    QMessageBox.critical(self, '错误', '删除发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)



                self.showBranchs()
                self.chooseBranch()


    def saveBranch(self):
        if self.bState == branchState.edit:
            if not self.ui.branchAsertLineEdit.text():
                self.ui.branchAsertLineEdit.setText('0')
            try:
                s = "update Branch set BranchName = '%s', City = '%s', Property = %s where BranchID = '%s';" % (self.ui.branchNameLineEdit.text(), self.ui.branchCityLineEdit.text(), self.ui.branchAsertLineEdit.text(), self.ui.branchIDLineEdit.text())
                self.dbcursor.execute(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '修改发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)


            self.showBranchs()
            self.chooseBranch()


        if self.bState == branchState.add:
            if not self.ui.branchAsertLineEdit.text():
                self.ui.branchAsertLineEdit.setText('0')
            try:
                s = "insert into Branch values ('%s', '%s', '%s', %s);"%(self.ui.branchIDLineEdit.text(), self.ui.branchNameLineEdit.text(), self.ui.branchCityLineEdit.text(), self.ui.branchAsertLineEdit.text())
                self.dbcursor.execute(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '新增发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)
            self.showBranchs()
            self.chooseBranch()
#branch