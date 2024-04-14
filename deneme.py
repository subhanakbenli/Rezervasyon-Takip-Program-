import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox


class MyTableWidget(QTableWidget):
    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checkbox Table Widget')
        self.setGeometry(100, 100, 600, 400)
        self.setRowCount(5)
        self.setColumnCount(3)

        for i in range(5):
            for j in range(3):
                item = QTableWidgetItem()
                checkbox = QCheckBox()
                checkbox.stateChanged.connect(self.checkboxChanged)
                self.setCellWidget(i, j, checkbox)

    def checkboxChanged(self, state):
        checkbox = self.sender()
        if checkbox.isChecked():
            checkbox.setText('Checked')
        else:
            checkbox.setText('Unchecked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tableWidget = MyTableWidget(5, 3)
    tableWidget.show()
    sys.exit(app.exec_())
