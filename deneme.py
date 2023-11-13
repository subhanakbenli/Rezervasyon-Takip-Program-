import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Silme Butonu ve Genişlik Örneği")
        self.setGeometry(100, 100, 600, 400)

        # QTableWidget oluştur
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Sütun 1", "Sütun 2", "Silme Butonu"])
        
        # Örnek veri ve silme butonu ekle
        for row in range(5):
            self.tableWidget.insertRow(row)
            
            # Örnek veri ekle
            for col in range(2):
                item = QTableWidgetItem(f"Satır {row+1}, Sütun {col+1}")
                self.tableWidget.setItem(row, col, item)
            
            # Silme butonu ekle
            delete_button = QPushButton("Sil", self)
            delete_button.clicked.connect(self.delete_row)
            self.tableWidget.setCellWidget(row, 2, delete_button)
            
            # Butonun genişliğini ayarla
            delete_button.setMaximumWidth(80)
            self.tableWidget.setColumnWidth(2,100)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def delete_row(self):
        # Silme butonuna tıklandığında çalışacak fonksiyon
        button = self.sender()
        if button:
            index = self.tableWidget.indexAt(button.pos())
            if index.isValid():
                # Sütunu sil
                self.tableWidget.removeRow(index.row())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())