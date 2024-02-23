# aaa="""Atv Turu
# Balon Turu 
# Araç Kiralama
# Scooter Kiralama
# Türk Gecesi
# Fotoğraf Çekimi
# Kiralik Elbise
# Jeep Safari
# At Turu 
# Derviş Gösterimi
# Yeşil Tur 
# Kırmızı Tur
# """
# print(aaa.split("\n"))

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Pencere Arkaya Alınma Uyarısı')

        button = QPushButton('Çıkış', self)
        button.clicked.connect(self.showExitDialog)
        button.setGeometry(100, 100, 100, 30)

    def showExitDialog(self):
        # Kullanıcıya onay almak için bir uyarı penceresi göster
        reply = QMessageBox.question(self, 'Uyarı', 'Pencereyi kapatmak istediğinizden emin misiniz?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Kullanıcı Evet'i seçtiyse pencereyi kapat
            self.close()

    def closeEvent(self, event):
        # Pencere kapatılmadan önce closeEvent tetiklenir
        self.showExitDialog()  # Kullanıcıya onay almak için uyarı penceresi göster
        event.ignore()  # Kapatma işlemini iptal et

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

