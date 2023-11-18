import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Editable Table Widget')

        # Tablo oluştur
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        # Hücrelere başlangıç değerleri ekle
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f'Row {row}, Col {col}')
                self.tableWidget.setItem(row, col, item)

        # Belirli hücreleri değiştirilemez yap
        self.tableWidget.item(1, 1).setFlags(self.tableWidget.item(1, 1).flags() ^ 2)  # ~Qt.ItemIsEditable

        # Layout oluştur
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MyTableWidget()
    window.setGeometry(100, 100, 600, 400)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
