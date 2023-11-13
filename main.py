# sübhan akbenli    
import sqlite3
from PyQt5.QtWidgets import *
import sys
from datetime import datetime,timedelta
from ui_designs.rezTakip_ui import * 

Uygulama = QApplication(sys.argv)
rezTakip_main_window = QMainWindow()
rezTakip_ui = Ui_rezTakip_MainWindow()
rezTakip_ui.setupUi(rezTakip_main_window)

class rezTakip():
    def __init__(self):
        self.conn=sqlite3.connect("database.db")
        self.curs=self.conn.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS aktiviteler (aktivite Text PRIMARY KEY,fiyat FLOAT,paraBirimi text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS rezervasyonlar \
                        (ID INTEGER  PRIMARY KEY AUTOINCREMENT,\
                        aktivite Text ,otelAdı Text,adSoyad TEXT,rezDate DATE,telefon TEXT,fiyat FLOAT,paraBirimi text)")
        
        rezTakip_ui.aktiviteListele_pushButton.clicked.connect(lambda : self.sqlden_cagir_tabloya_dok("aktiviteler",rezTakip_ui.aktivite_tableWidget))
        rezTakip_ui.rezervasyonListele_pushButton.clicked.connect(lambda : self.sqlden_cagir_tabloya_dok("rezervasyonlar",rezTakip_ui.rezervasyon_tableWidget))
    def sqlden_cagir_tabloya_dok(self,tablo_adi,tablo):
        self.curs.execute(f"SELECT * FROM {tablo_adi}")
        data=self.curs.fetchall()
        tabloya_dok(tablo,data)
        
    def aktivite_ekle(self):
        sql_tabloya_ekle(self.conn,self.curs,"aktiviteler",[("asd","150","tl")])
                    
def sql_tabloya_ekle(conn,curs,tabloadi,veri):
    soru_isareti_sayisi=(len(veri)*'?,').strip(",")
    curs.execute(f"INSERT INTO {tabloadi} VALUES({soru_isareti_sayisi})",(veri))
    conn.commit()
    print(veri)

def tabloya_dok(tablo, satirlar):
    """
    Tabloya verilen satırları ekleyen fonksiyon.

    :param tablo: QTableWidget nesnesi
    :param satirlar: Liste içinde satırlar. Her bir satır da bir liste olmalıdır.
    """
        
    tablo.setRowCount(len(satirlar))
    # Tabloya satırları eklemek için döngü
    for satir_index, satir in enumerate(satirlar):
        # son sütuna sil butonu ekleyip boyutlandırmak için
        son=tablo.columnCount()-1
        delete_button = QPushButton("Sil")
        delete_button.clicked.connect(lambda : satir_sil())
        delete_button.setStyleSheet("background-color: rgb(235,105,105)")
        delete_button.setMaximumWidth(125)        
        tablo.setCellWidget(satir_index, son, delete_button)
        tablo.setColumnWidth(son, 125) 
        # Her bir hücreyi eklemek için döngü        
        for sutun_index, hucre_verisi in enumerate(satir):
            hucre = QTableWidgetItem(str(hucre_verisi))
            # Tabloya ekle
            tablo.setItem(satir_index, sutun_index, hucre)   
            
            if tablo == rezTakip_ui.aktivite_tableWidget:           
                if sutun_index==0:          tablo.setColumnWidth(sutun_index, 450)
                else:                       tablo.setColumnWidth(sutun_index, 305) 
                    
            elif tablo == rezTakip_ui.rezervasyon_tableWidget:
                if sutun_index==0:          tablo.setColumnWidth(sutun_index, 90)
                elif sutun_index==7:        tablo.setColumnWidth(sutun_index, 100)
                else:                       tablo.setColumnWidth(sutun_index, 145) 
            elif tablo == rezTakip_ui.musteri_tableWidget:
                pass
def satir_sil():
    print("asdasd")
rezTakip()
rezTakip_ui.aktiviteListele_pushButton.click()
rezTakip_ui.musterilerListele_pushButton.click()
rezTakip_ui.rezervasyonListele_pushButton.click()
rezTakip_main_window.show()
sys.exit(Uygulama.exec_())