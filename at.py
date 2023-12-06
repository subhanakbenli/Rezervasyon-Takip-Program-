import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QDateEdit
from PyQt5.QtCore import QDate, Qt

class DateEditExample(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layout oluştur
        layout = QVBoxLayout()

        # Bugünkü tarihi gösteren DateEdit
        self.today_date_edit = QDateEdit(self)
        self.today_date_edit.setCalendarPopup(True)
        self.today_date_edit.setDate(QDate.currentDate())
        self.today_date_edit.dateChanged.connect(self.on_date_changed)

        layout.addWidget(QLabel("Bugünün Tarihi:"))
        layout.addWidget(self.today_date_edit)

        # Yarının tarihini gösteren DateEdit
        self.tomorrow_date_edit = QDateEdit(self)
        self.tomorrow_date_edit.setCalendarPopup(True)
        self.tomorrow_date_edit.setDate(QDate.currentDate().addDays(1))

        layout.addWidget(QLabel("Yarının Tarihi:"))
        layout.addWidget(self.tomorrow_date_edit)

        # Ana pencereye layout'u yerleştir
        self.setLayout(layout)

        # Pencereyi ayarla
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('DateEdit Örneği')
        self.show()

    def on_date_changed(self, date):
        # Bugünkü tarih değiştikçe, yarının tarihini güncelle
        tomorrow_date = date.addDays(1)
        self.tomorrow_date_edit.setDate(tomorrow_date)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DateEditExample()
    sys.exit(app.exec_())
