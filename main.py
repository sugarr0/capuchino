import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog, QDialog, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.cursor = sqlite3.connect("coffee.db")
        self.add.clicked.connect(self.append)
        self.update.clicked.connect(self.edit)
        self.see()

    def see(self):
        cursor = self.cursor.cursor()
        data = cursor.execute("SELECT * FROM coffee").fetchall()
        if not data:
            return
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        title = [description[0] for description in cursor.description]
        for i, elem in enumerate(data):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setHorizontalHeaderLabels(title)

    def append(self):
        form = AddEdit(self)
        form.exec()

    def edit(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if len(rows) != 1:
            QMessageBox.question(self, '', "Выберите 1 элемент",
                                        QMessageBox.Ok)
            return
        inf = self.tableWidget.item(rows[0], 0).text()
        form = AddEdit(self, inf)
        form.exec()

    def upd(self, res):
        print(res)


class AddEdit(QDialog):
    def __init__(self, other, inf=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.accept_my)
        self.pushButton_2.clicked.connect(self.reject)
        self.inf = None
        self.other = other
        if inf:
            cursor = sqlite3.connect("coffee.db").cursor()
            data = cursor.execute("SELECT * FROM coffee WHERE id = ?", inf).fetchall()
            self.lineEdit.setText(data[0][1])
            self.lineEdit_2.setText(data[0][2])
            self.textEdit.setText(data[0][4])
            self.spinBox.setValue(data[0][5])
            self.spinBox_2.setValue(data[0][6])
            self.inf = inf
            if self.comboBox.currentText() != data[0][3]:
                self.comboBox.setItemText(1, self.comboBox.currentText())
                self.comboBox.setItemText(0, data[0][3])

    def accept_my(self):
        ret = (self.inf, self.lineEdit.text(), self.lineEdit_2.text(), self.comboBox.currentText(),
               self.textEdit.toPlainText(), self.spinBox.text(), self.spinBox_2.text())
        if '' in (ret[1], ret[2], ret[4]) or '0' in (ret[5], ret[6]):
            QMessageBox.question(self, '', "Заполните все поля",
                                 QMessageBox.Ok)
            return
        self.other.upd(ret)
        self.reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
