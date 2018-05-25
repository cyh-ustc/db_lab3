# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QDate


from bank import Ui_MainWindow
import pymysql

from enum import Enum


searchPre = [' = \'', ' <> \'', ' like \'%']
searchPost = ['\'', '\'', '%\'']
searchIn = ['>', '>=', '=', '<=', '<', '<>']

accountInfo = ['账户号', '类型', '支行号', '支行名', '身份证号', '姓名', '余额', '透支额度', '利率', '开户日期', '最近访问日期', '负责人身份证号', '负责人姓名', '币种']
accountWidth = [80, 40, 60, 80, 140, 60, 80, 80, 80, 120, 120, 140, 80, 60]


branchInfo = ['支行号', '支行名', '城市', '资产']
branchWidth = [60, 80, 60, 120]


employeeInfo = ['身份证号', '姓名', '电话', '地址', '开始工作日期']
employeeWidth = [140, 60, 100, 60, 120]
employeeCol = ['EmployeeID', 'EmployeeName', 'EmployeeTele', 'EmployeeAddress', 'StartWork']



customerInfo = ['身份证号', '姓名', '电话', '地址', '联系人姓名', '联系人电话', '联系人电子邮件地址', '联系人与客户关系']
customerCol = ['CustomerID', 'CustomerName', 'Tele', 'Address', 'ContactName', 'ContactTele', 'ContactEmail', 'Relationship']
customerWidth = [140, 60, 100, 60, 60, 100, 160, 140]






class State(Enum):
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
        self.connectSignals()



#branch
        self.branchSearchCondition = '1'
        self.showBranchs()
        self.bState = State.notchosen
        self.ui.branchTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
#branch

# employee
        self.showEmployee()
        self.eState = State.notchosen
        self.employeeEdits = [self.ui.employeeIDLineEdit, self.ui.employeeNameLineEdit, self.ui.employeeTeleLineEdit, self.ui.employeeAddressLineEdit, self.ui.employeeSDateEdit]
        self.ui.employeeTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
# employee

#account

        self.accountSearchCondition = '1'
        self.showAccount();
        self.aState = State.notchosen

#account


#customer
        self.cState = State.notchosen
        self.showCustomers()
        self.customerLineEdits = [self.ui.customerIDLineEdit, self.ui.customerNameLineEdit, self.ui.customerTeleLineEdit, self.ui.customerAddressLineEdit, self.ui.contactNameLineEdit, self.ui.contactTeleLineEdit, self.ui.contactEmailLineEdit, self.ui.contactRelationshipLineEdit]
        self.ui.customerTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
#customer




    def connectSignals(self):
        #account

        #account

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
        self.ui.branchSearchPushButton.clicked.connect(self.updateBranchSearchCondition)
        #branch

        #employee
        self.ui.employeeSearchPushButton.clicked.connect(self.showEmployee)
        self.ui.employeeSearchSDateCheckBox.stateChanged.connect(self.employeeSearchConditionChanged)
        self.ui.employeeSearchIDCheckBox.stateChanged.connect(self.employeeSearchConditionChanged)
        self.ui.employeeSearchNameCheckBox.stateChanged.connect(self.employeeSearchConditionChanged)
        self.ui.employeeSearchInfoCheckBox.stateChanged.connect(self.employeeSearchConditionChanged)
        self.ui.employeeTableView.clicked.connect(self.chooseEmployee)
        self.ui.employeeAlterPushButton.clicked.connect(self.editEmployee)
        self.ui.employeeAbortPushButton.clicked.connect(self.abortEmployee)
        self.ui.employeeAddPushButton.clicked.connect(self.addEmployee)
        self.ui.employeeSavePushButton.clicked.connect(self.saveEmployee)
        self.ui.employeeDeletePushButton.clicked.connect(self.deleteEmployee)
        #employee

        #customer
        self.ui.customerTableView.clicked.connect(self.chooseCustomer)
        self.ui.customerSearchCustomerIDCheckBox.stateChanged.connect(self.customerSearchConditionChanged)
        self.ui.customerSearchCustomerNameCheckBox.stateChanged.connect(self.customerSearchConditionChanged)
        self.ui.customerSearchOtherInfoCheckBox.stateChanged.connect(self.customerSearchConditionChanged)
        self.ui.customerSearchPushButton.clicked.connect(self.showCustomers)
        self.ui.customerAlterPushButton.clicked.connect(self.editCustomer)
        self.ui.customerAbortPushButton.clicked.connect(self.abortCustomer)
        self.ui.customerAddPushButton.clicked.connect(self.addCustomer)
        self.ui.customerSavePushButton.clicked.connect(self.saveCustomer)
        self.ui.customerDeletePushButton.clicked.connect(self.deleteCustomer)
        #customer

    def connectDB(self):
        self.db = pymysql.connect('localhost', 'root', '135565', 'bank')
        self.dbcursor = self.db.cursor()

#account
    def showAccount(self):
        self.dbcursor.execute('select * from accountview where %s;' % self.accountSearchCondition)
        results = self.dbcursor.fetchall()
        self.accountModel = QStandardItemModel(self.ui.accountTableView)
        self.accountModel.setRowCount(len(results))
        self.accountModel.setColumnCount(14)
        for i in range(14):
            self.accountModel.setHeaderData(i, Qt.Horizontal, accountInfo[i])
        self.ui.accountTableView.setModel(self.accountModel)
        for i in range(14):
            w = self.ui.accountTableView.width()
            self.ui.accountTableView.setColumnWidth(i, accountWidth[i])
        for i in range(len(results)):
            for j in range(14):
                self.accountModel.setItem(i, j, QStandardItem(str(results[i][j])))
        for i in range(len(results)):
            self.accountModel.item(i, 6).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.accountModel.item(i, 7).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.accountModel.item(i, 8).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)




#account



#employee
    def showEmployee(self):
        cd = '1'
        if self.ui.employeeSearchIDCheckBox.isChecked():
            idx = self.ui.employeeSearchIDComboBox.currentIndex()
            cd += ' and EmployeeID%s%s%s'%(searchPre[idx], self.ui.employeeSearchIDLineEdit.text() , searchPost[idx])
        if self.ui.employeeSearchNameCheckBox.isChecked():
            idx = self.ui.employeeSearchNameComboBox.currentIndex()
            cd += ' and EmployeeName%s%s%s'%(searchPre[idx], self.ui.employeeSearchNameLineEdit.text() , searchPost[idx])
        if self.ui.employeeSearchInfoCheckBox.isChecked():
            s = self.ui.employeeSearchInfoLineEdit.text()
            cd += ' and (EmployeeTele like \'%%%s%%\' or EmployeeAddress like \'%%%s%%\')'%(s, s)
        if self.ui.employeeSearchSDateCheckBox.isChecked():
            idx = self.ui.employeeSearchSDateComboBox.currentIndex()
            s = '\'' + self.ui.employeeSearchSDateEdit.text() + '\''
            cd += ' and StartWork ' + searchIn[idx] + s

        s = 'select * from Employee where %s;'%cd
        print(s)
        self.dbcursor.execute(s)
        results = self.dbcursor.fetchall()
        self.employeeModel = QStandardItemModel(self.ui.employeeTableView)
        self.employeeModel.setRowCount(len(results))
        self.employeeModel.setColumnCount(5)
        for i in range(5):
            self.employeeModel.setHeaderData(i, Qt.Horizontal, employeeInfo[i])
        self.ui.employeeTableView.setModel(self.employeeModel)
        for i in range(5):
            w = self.ui.employeeTableView.width()
            self.ui.employeeTableView.setColumnWidth(i,  employeeWidth[i])
        for i in range(len(results)):
            for j in range(5):
                self.employeeModel.setItem(i, j, QStandardItem(str(results[i][j])))


    def employeeSearchConditionChanged(self):
        if self.ui.employeeSearchIDCheckBox.isChecked():
            self.ui.employeeSearchIDComboBox.setEnabled(True)
            self.ui.employeeSearchIDLineEdit.setEnabled(True)
        else:
            self.ui.employeeSearchIDComboBox.setEnabled(False)
            self.ui.employeeSearchIDLineEdit.setEnabled(False)

        if self.ui.employeeSearchNameCheckBox.isChecked():
            self.ui.employeeSearchNameComboBox.setEnabled(True)
            self.ui.employeeSearchNameLineEdit.setEnabled(True)
        else:
            self.ui.employeeSearchNameComboBox.setEnabled(False)
            self.ui.employeeSearchNameLineEdit.setEnabled(False)

        if self.ui.employeeSearchInfoCheckBox.isChecked():
            self.ui.employeeSearchInfoComboBox.setEnabled(True)
            self.ui.employeeSearchInfoLineEdit.setEnabled(True)
        else:
            self.ui.employeeSearchInfoComboBox.setEnabled(False)
            self.ui.employeeSearchInfoLineEdit.setEnabled(False)

        if self.ui.employeeSearchSDateCheckBox.isChecked():
            self.ui.employeeSearchSDateComboBox.setEnabled(True)
            self.ui.employeeSearchSDateEdit.setEnabled(True)
        else:
            self.ui.employeeSearchSDateComboBox.setEnabled(False)
            self.ui.employeeSearchSDateEdit.setEnabled(False)

    def chooseEmployee(self):
        ix = self.ui.employeeTableView.currentIndex()
        if ix.row() != -1:
            for i in range(4):
                idx = self.employeeModel.index(ix.row(), i)
                self.employeeEdits[i].setText(self.employeeModel.data(idx))
            idx = self.employeeModel.index(ix.row(), 4)
            self.ui.employeeSDateEdit.setDate(QDate().fromString(self.employeeModel.data(idx), "yyyy-MM-dd"))
            self.eState = State.chosen
        else:
            for i in range(4):
                self.employeeEdits[i].setText('')

            self.eState = State.notchosen
        for i in range(5):
            self.employeeEdits[i].setEnabled(False)
        self.ui.employeeAddPushButton.setEnabled(True)
        self.ui.employeeAlterPushButton.setEnabled(True)
        self.ui.employeeDeletePushButton.setEnabled(True)
        self.ui.employeeTableView.setEnabled(True)

    def editEmployee(self):
        if self.eState == State.chosen:
            self.eState = State.edit
            self.ui.employeeTableView.setEnabled(False)
            self.ui.employeeAddPushButton.setEnabled(False)
            self.ui.employeeAlterPushButton.setEnabled(False)
            self.ui.employeeDeletePushButton.setEnabled(False)
            self.ui.employeeIDLineEdit.setEnabled(False)
            for i in range(1, 5):
                self.employeeEdits[i].setEnabled(True)

    def abortEmployee(self):
        for i in range(5):
            self.employeeEdits[i].setEnabled(False)
        self.chooseEmployee()


    def addEmployee(self):
        if self.eState == State.chosen or self.eState == State.notchosen:
            self.eState = State.add

            for i in range(4):
                self.employeeEdits[i].setText('')
                self.employeeEdits[i].setEnabled(True)
            self.ui.employeeSDateEdit.setEnabled(True)

    def saveEmployee(self):
        if self.eState == State.edit:
            try:
                s = 'update Employee set '
                for i in range(1, 5):
                    s += "%s = '%s', "%(employeeCol[i], self.employeeEdits[i].text())
                s = s[:-2]
                s += " where EmployeeID = '%s';"%self.employeeEdits[0].text()
                self.dbcursor.execute(s)
                print(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '修改发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)

        elif self.eState == State.add:
            try:
                s = 'insert into Employee values ('
                for i in range(5):
                    s += "'%s', "%self.employeeEdits[i].text()
                s = s[:-2]
                s += ");"
                self.dbcursor.execute(s)
                print(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '新增发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)

        self.showEmployee()
        self.chooseEmployee()

    def deleteEmployee(self):
        if self.eState == State.chosen:
            dID = self.ui.employeeIDLineEdit.text()
            q = QMessageBox.question(self, '删除一条记录', '确认删除这条记录吗？\r\n身份证号为%s'%dID, QMessageBox.Yes, QMessageBox.No)
            if q == QMessageBox.Yes:
                try:
                    s = "delete from Employee where EmployeeID = '%s'"%dID
                    self.dbcursor.execute(s)
                    self.db.commit()

                except Exception as e:
                    self.db.rollback()
                    QMessageBox.critical(self, '错误', '删除发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)

                self.showEmployee()
                self.chooseEmployee()
#employee


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


    def updateBranchSearchCondition(self):
        if self.ui.branchSearchRangeComboBox.currentIndex() == 0:
            self.branchSearchCondition = '1'
        if self.ui.branchSearchBranchIDCheckBox.isChecked():
            idx = self.ui.branchSearchBranchIDComboBox.currentIndex()
            self.branchSearchCondition += ' and BranchID' + searchPre[idx] + self.ui.branchSearchBranchIDLineEdit.text() + searchPost[idx]
        if self.ui.branchSearchBranchNameCheckBox.isChecked():
            idx = self.ui.branchSearchBranchNameComboBox.currentIndex()
            self.branchSearchCondition += ' and BranchName' + searchPre[idx] + self.ui.branchSearchBranchNameLineEdit.text() + searchPost[idx]
        if self.ui.branchSearchCityCheckBox.isChecked():
            idx = self.ui.branchSearchCityComboBox.currentIndex()
            self.branchSearchCondition += ' and City' + searchPre[idx] + self.ui.branchSearchCityLineEdit.text() + searchPost[idx]
        if self.ui.branchSearchAssetCheckBox.isChecked():
            idx = self.ui.branchSearchAssetComboBox.currentIndex()
            if not self.ui.branchSearchAssetLineEdit.text():
                self.ui.branchSearchAssetLineEdit.setText('0')
            self.branchSearchCondition += ' and Property' + searchIn[idx] + self.ui.branchSearchAssetLineEdit.text()
        print(self.branchSearchCondition)
        self.showBranchs()


    def showBranchs(self):
        self.dbcursor.execute('select * from Branch where %s;'%self.branchSearchCondition)
        results = self.dbcursor.fetchall()
        #self.ui.branchTableView
        self.branchModel = QStandardItemModel(self.ui.branchTableView)
        self.branchModel.setRowCount(len(results))
        self.branchModel.setColumnCount(4)
        for i in range(4):
            self.branchModel.setHeaderData(i, Qt.Horizontal, branchInfo[i])
        self.ui.branchTableView.setModel(self.branchModel)
        for i in range(4):
            w = self.ui.branchTableView.width()
            self.ui.branchTableView.setColumnWidth(i, branchWidth[i])
        for i in range(len(results)):
            for j in range(4):
                self.branchModel.setItem(i, j, QStandardItem(str(results[i][j])))
        for i in range(len(results)):
            self.branchModel.item(i, 3).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)



    def chooseBranch(self):
        i = self.ui.branchTableView.currentIndex()
        if i.row() != -1:
            idx = self.branchModel.index(i.row(), 0)
            self.ui.branchIDLineEdit.setText(self.branchModel.data(idx))
            idx = self.branchModel.index(i.row(), 1)
            self.ui.branchNameLineEdit.setText(self.branchModel.data(idx))
            idx = self.branchModel.index(i.row(), 2)
            self.ui.branchCityLineEdit.setText(self.branchModel.data(idx))
            idx = self.branchModel.index(i.row(), 3)
            self.ui.branchAsertLineEdit.setText(self.branchModel.data(idx))

            self.bState = State.chosen
            self.ui.branchTableView.setEnabled(True)

        else:
            self.ui.branchIDLineEdit.setText('')
            self.ui.branchNameLineEdit.setText('')
            self.ui.branchCityLineEdit.setText('')
            self.ui.branchAsertLineEdit.setText('')
            self.bState = State.notchosen
            self.ui.branchTableView.setEnabled(True)
            self.ui.branchIDLineEdit.setEnabled(False)
            self.ui.branchNameLineEdit.setEnabled(False)
            self.ui.branchCityLineEdit.setEnabled(False)
            self.ui.branchAsertLineEdit.setEnabled(False)

        self.ui.addBranchPushButton.setEnabled(True)
        self.ui.editBranchPushButton.setEnabled(True)
        self.ui.deleteBranchPushButton.setEnabled(True)

    def editBranch(self):
        if self.bState == State.chosen:
            self.bState = State.edit
            self.ui.branchTableView.setEnabled(False)
            self.ui.addBranchPushButton.setEnabled(False)
            self.ui.editBranchPushButton.setEnabled(False)
            self.ui.deleteBranchPushButton.setEnabled(False)
            self.ui.branchIDLineEdit.setEnabled(False)
            self.ui.branchNameLineEdit.setEnabled(True)
            self.ui.branchCityLineEdit.setEnabled(True)
            self.ui.branchAsertLineEdit.setEnabled(True)

    def abortBranch(self):
        if self.bState == State.edit:
            self.bState = State.chosen
            self.chooseBranch()
        elif self.bState == State.add:
            self.bState = State.notchosen
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
        if self.bState == State.chosen or self.bState == State.notchosen:
            self.bState = State.add
            self.ui.branchIDLineEdit.setText('')
            self.ui.branchNameLineEdit.setText('')
            self.ui.branchCityLineEdit.setText('')
            self.ui.branchAsertLineEdit.setText('')
            self.ui.branchIDLineEdit.setEnabled(True)
            self.ui.branchNameLineEdit.setEnabled(True)
            self.ui.branchCityLineEdit.setEnabled(True)
            self.ui.branchAsertLineEdit.setEnabled(True)

    def deleteBranch(self):
        if self.bState == State.chosen:
            dID = self.ui.branchIDLineEdit.text()
            q = QMessageBox.question(self, '删除一条记录', '确认删除这条记录吗？\r\n支行号：%s'%dID, QMessageBox.Yes, QMessageBox.No)
            if q == QMessageBox.Yes:
                try:
                    s = "delete from Branch where BranchID = '%s'"%dID
                    self.dbcursor.execute(s)
                    self.db.commit()

                except Exception as e:
                    self.db.rollback()
                    QMessageBox.critical(self, '错误', '删除发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)



                self.showBranchs()
                self.chooseBranch()


    def saveBranch(self):
        if self.bState == State.edit:
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


        if self.bState == State.add:
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

#customer
    def customerSearchConditionChanged(self):
        if self.ui.customerSearchCustomerIDCheckBox.isChecked():
            self.ui.customerSearchCustomerIDComboBox.setEnabled(True)
            self.ui.customerSearchCustomerIDLineEdit.setEnabled(True)
        else:
            self.ui.customerSearchCustomerIDComboBox.setEnabled(False)
            self.ui.customerSearchCustomerIDLineEdit.setEnabled(False)

        if self.ui.customerSearchCustomerNameCheckBox.isChecked():
            self.ui.customerSearchCustomerNameComboBox.setEnabled(True)
            self.ui.customerSearchCustomerNameLineEdit.setEnabled(True)
        else:
            self.ui.customerSearchCustomerNameComboBox.setEnabled(False)
            self.ui.customerSearchCustomerNameLineEdit.setEnabled(False)

        if self.ui.customerSearchOtherInfoCheckBox.isChecked():
            self.ui.customerSearchOtherInfoComboBox.setEnabled(True)
            self.ui.customerSearchOtherInfoLineEdit.setEnabled(True)
        else:
            self.ui.customerSearchOtherInfoComboBox.setEnabled(False)
            self.ui.customerSearchOtherInfoLineEdit.setEnabled(False)


    def showCustomers(self):
        cd = '1'
        if self.ui.customerSearchCustomerIDCheckBox.isChecked():
            idx = self.ui.customerSearchCustomerIDComboBox.currentIndex()
            cd += ' and CustomerID%s%s%s'%(searchPre[idx], self.ui.customerSearchCustomerIDLineEdit.text() , searchPost[idx])
        if self.ui.customerSearchCustomerNameCheckBox.isChecked():
            idx = self.ui.customerSearchCustomerNameComboBox.currentIndex()
            cd += ' and CustomerName%s%s%s'%(searchPre[idx], self.ui.customerSearchCustomerNameLineEdit.text() , searchPost[idx])
        if self.ui.customerSearchOtherInfoCheckBox.isChecked():
            s = self.ui.customerSearchOtherInfoLineEdit.text()
            cd += ' and (Tele like \'%%%s%%\' or Address like \'%%%s%%\' or ContactName like \'%%%s%%\' or ContactTele like \'%%%s%%\' or ContactEmail like \'%%%s%%\' or Relationship like \'%%%s%%\')'%(s, s, s, s, s, s)

        s = 'select * from Customer where %s;'%cd
        print(s)
        self.dbcursor.execute(s)
        results = self.dbcursor.fetchall()
        self.customerModel = QStandardItemModel(self.ui.customerTableView)
        self.customerModel.setRowCount(len(results))
        self.customerModel.setColumnCount(8)
        for i in range(8):
            self.customerModel.setHeaderData(i, Qt.Horizontal, customerInfo[i])
        self.ui.customerTableView.setModel(self.customerModel)
        for i in range(8):
            w = self.ui.customerTableView.width()
            self.ui.customerTableView.setColumnWidth(i, customerWidth[i])
        for i in range(len(results)):
            for j in range(8):
                self.customerModel.setItem(i, j, QStandardItem(str(results[i][j])))



    def chooseCustomer(self):
        ix = self.ui.customerTableView.currentIndex()
        if ix.row() != -1:
            for i in range(8):
                idx = self.customerModel.index(ix.row(), i)
                self.customerLineEdits[i].setText(self.customerModel.data(idx))
            self.cState = State.chosen
        else:
            for i in range(8):
                self.customerLineEdits[i].setText('')
                self.customerLineEdits[i].setEnabled(False)
            self.cState = State.notchosen
        self.ui.customerTableView.setEnabled(True)
        self.ui.customerAddPushButton.setEnabled(True)
        self.ui.customerAlterPushButton.setEnabled(True)
        self.ui.customerDeletePushButton.setEnabled(True)

    def editCustomer(self):
        if self.cState == State.chosen:
            self.cState = State.edit
            self.ui.customerTableView.setEnabled(False)
            self.ui.customerAddPushButton.setEnabled(False)
            self.ui.customerAlterPushButton.setEnabled(False)
            self.ui.customerDeletePushButton.setEnabled(False)
            self.ui.customerIDLineEdit.setEnabled(False)
            for i in range(1, 8):
                self.customerLineEdits[i].setEnabled(True)

    def abortCustomer(self):
        for i in range(0, 8):
            self.customerLineEdits[i].setEnabled(False)
        self.chooseCustomer()


    def addCustomer(self):
        if self.cState == State.chosen or self.cState == State.notchosen:
            self.cState = State.add

            for i in range(8):
                self.customerLineEdits[i].setText('')
                self.customerLineEdits[i].setEnabled(True)

    def saveCustomer(self):
        if self.cState == State.edit:
            try:
                s = 'update Customer set '
                for i in range(1, 8):
                    s += "%s = '%s', "%(customerCol[i], self.customerLineEdits[i].text())
                s = s[:-2]
                s += " where CustomerID = '%s';"%self.customerLineEdits[0].text()
                self.dbcursor.execute(s)
                print(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '修改发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)

        elif self.cState == State.add:
            try:
                s = 'insert into Customer values ('
                for i in range(8):
                    s += "'%s', "%self.customerLineEdits[i].text()
                s = s[:-2]
                s += ");"
                self.dbcursor.execute(s)
                print(s)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, '错误', '新增发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)

        self.showCustomers()
        self.chooseCustomer()

    def deleteCustomer(self):
        if self.cState == State.chosen:
            dID = self.ui.customerIDLineEdit.text()
            q = QMessageBox.question(self, '删除一条记录', '确认删除这条记录吗？\r\n身份证号为%s'%dID, QMessageBox.Yes, QMessageBox.No)
            if q == QMessageBox.Yes:
                try:
                    s = "delete from Customer where CustomerID = '%s'"%dID
                    self.dbcursor.execute(s)
                    self.db.commit()

                except Exception as e:
                    self.db.rollback()
                    QMessageBox.critical(self, '错误', '删除发生了错误\r\n错误码：%d\r\n%s\r\n'%e.args + s)



                self.showCustomers()
                self.chooseCustomer()

#customer