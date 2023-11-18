# sübhan akbenli    
import sqlite3
from PyQt5.QtWidgets import *
import sys
from datetime import datetime,timedelta
from ui_designs.rezTakip_ui import * 

TABLO_AKTIVITELER="aktiviteler"
INSERT_AKTIVITELER="(aktivite,TL,DOLAR,EURO,KART)"

TABLO_REZERVASYONLAR="rezervasyonlar"
INSERT_REZERVASYONLAR="(aktivite,otelAdi,adSoyad,rezDate,telefon,fiyat,paraBirimi)"

TABLO_MUSTERILER="musteriler"
INSERT_MUSTERILER="(otelAdi,telefon,odenen,kalan,Toplam)"

Uygulama = QApplication(sys.argv)
rezTakip_main_window = QMainWindow()
rezTakip_ui = Ui_rezTakip_MainWindow()
rezTakip_ui.setupUi(rezTakip_main_window)
rezTakip_ui.statusbar.setStyleSheet("font: 75 13pt 'Times New Roman'; background-color:rgb(200,200,200)")
class CustomSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(0, 9999999)
    def wheelEvent(self, event):
        # Fare tekerleği olaylarını engelle
        event.ignore()

class rezTakip():
    def __init__(self):
        self.conn=sqlite3.connect("database.db")
        self.curs=self.conn.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS aktiviteler (aktivite Text PRIMARY KEY,TL FLOAT,DOLAR FLOAT,EURO FLOAT,KART FLOAT)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS rezervasyonlar \
                        (rezID INTEGER  PRIMARY KEY AUTOINCREMENT,aktivite Text ,otelAdi Text,\
                            adSoyad TEXT,rezDate DATE,telefon TEXT,fiyat FLOAT,paraBirimi text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS musteriler \
                        (otelAdi Text PRIMARY KEY,telefon Text,odenen FLOAT,kalan FLOAT,Toplam FLOAT)")
        rezTakip_ui.aktiviteListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_AKTIVITELER,rezTakip_ui.aktivite_tableWidget))
        rezTakip_ui.rezervasyonListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget))
        self.aktivite_ekle()
        rezTakip_ui.musterilerListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_MUSTERILER,rezTakip_ui.musteri_tableWidget) )
        rezTakip_ui.rezYap_pushButton.clicked.connect(lambda : 
            self.satir_ekle_aktivite(rezTakip_ui.rezervasyon_tableWidget))
        rezTakip_ui.aktEkle_pushButton.clicked.connect(lambda : 
            self.satir_ekle_aktivite(rezTakip_ui.aktivite_tableWidget))
        
    def satir_ekle_aktivite(self,tablo):
        row=tablo.rowCount()
        tablo.setRowCount(row+1)
        son=tablo.columnCount()-1
        save_button = QPushButton("Kaydet")
        save_button.setStyleSheet("background-color: rgb(105,255,105)")
        save_button.setMaximumWidth(125)        
        tablo.setCellWidget(row, son, save_button)
        if tablo ==     rezTakip_ui.aktivite_tableWidget:   save_button.clicked.connect(lambda : self.aktivite_kaydet)
        elif tablo == rezTakip_ui.rezervasyon_tableWidget:  save_button.clicked.connect(lambda : self.rezervasyon_kaydet )

    def aktivite_kaydet():    
        print("aktivite")

    def rezervasyon_kaydet():
        print("rezervasyon")

    def musteri_kaydet():    
        print("musteri")

    def aktivite_ekle(self):
        sql_tabloya_ekle(self.conn,self.curs, TABLO_AKTIVITELER, ("asd",1500,150,125,1700))
        sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_AKTIVITELER,rezTakip_ui.aktivite_tableWidget)
    
    def rezervasyon_ekle(self):
        sql_tabloya_ekle(self.conn,self.curs, f"{TABLO_REZERVASYONLAR} {INSERT_REZERVASYONLAR}", ("asd","otelim","NİL DENİZ ÇETİNKAYA","2023-09-09","05522612829",875.5,"EURO"))
        sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget)              
    
    def musteri_ekle(self):
        # sql_tabloya_ekle(self.conn,self.curs, f"{TABLO_MUSTERILER} {INSERT_MUSTERILER}", ("otelim","05522612829",875.5,875.5,1756))
        sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_MUSTERILER,rezTakip_ui.musteri_tableWidget)    
    
    
    
def sql_tabloya_ekle(conn,curs,tabloadi,veri):
    try:
        soru_isareti_sayisi=(len(veri)*'?,').strip(",")
        curs.execute(f"INSERT INTO {tabloadi} VALUES({soru_isareti_sayisi})",(veri))
        conn.commit()
    except    sqlite3.IntegrityError:
        uyari_ver("Bu otel adı daha önceden eklendi",5000)
    except:
        uyari_ver("!! Beklenmeyen bir hata oluştu !!")




def sqlden_cagir_tabloya_dok(conn,curs,tablo_adi,tablo):
        curs.execute(f"SELECT * FROM {tablo_adi}")
        data=curs.fetchall()
        tabloya_dok(conn,curs,tablo,data)

def tabloya_dok(conn,curs,tablo, satirlar):
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
        delete_button.setStyleSheet("background-color: rgb(235,105,105)")
        delete_button.setMaximumWidth(100)    
        update_button = QPushButton("Güncelle")
        update_button.setStyleSheet("background-color: rgb(105,185,185)")
        update_button.setMaximumWidth(100)     

        tablo.setCellWidget(satir_index, son-1, update_button)
        tablo.setCellWidget(satir_index, son, delete_button)
        tablo.setColumnWidth(son-1, 110) 
        tablo.setColumnWidth(son, 100) 
        
        if tablo == rezTakip_ui.aktivite_tableWidget:       
            update_button.clicked.connect(lambda : sql_tablo_update_aktivite(conn,curs))
            delete_button.clicked.connect(lambda : satir_sil_aktivite(conn,curs))         
        elif tablo == rezTakip_ui.rezervasyon_tableWidget:  
            # update_button.clicked.connect(lambda : sql)
            delete_button.clicked.connect(lambda : satir_sil_rezervasyon(conn,curs))
        # elif tablo == rezTakip_ui.musteri_tableWidget:      delete_button.clicked.connect(lambda : satir_sil_musteri())
        
        # Her bir hücreyi eklemek için döngü        
        for sutun_index, hucre_verisi in enumerate(satir):
             
            if tablo == rezTakip_ui.aktivite_tableWidget:         
                    
                if sutun_index==0:          
                    hucre = QTableWidgetItem(str(hucre_verisi))
                    tablo.setItem(satir_index, sutun_index, hucre)                      
                    tablo.setColumnWidth(sutun_index, 450)
                    item = QTableWidgetItem(f'Row {satir_index}, Col {sutun_index}')
                    item.setFlags(item.flags() ^ 2) ### burayı incele
                elif 0<sutun_index<5:
                    spin_box=CustomSpinBox()
                    spin_box.setValue(float(hucre_verisi))
                    spin_box.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    tablo.setCellWidget(satir_index, sutun_index,spin_box)
                    tablo.setColumnWidth(sutun_index, 175) 
                else:                       tablo.setColumnWidth(sutun_index, 150) 
                
            elif tablo == rezTakip_ui.rezervasyon_tableWidget:
                hucre = QTableWidgetItem(str(hucre_verisi))
                # Tabloya ekle
                tablo.setItem(satir_index, sutun_index, hucre)  
                if sutun_index==0:        
                    tablo.setColumnWidth(sutun_index, 50)
                    item = QTableWidgetItem(f'Row {satir_index}, Col {sutun_index}')
                    item.setFlags(item.flags() ^ 2) ### burayı incele
                elif sutun_index==7 or sutun_index==6:          
                    tablo.setColumnWidth(sutun_index, 105)
                    item = QTableWidgetItem(f'Row {satir_index}, Col {sutun_index}')
                    item.setFlags(item.flags() ^ 2) ### burayı incele
                elif sutun_index == 4 :     tablo.setColumnWidth(sutun_index, 150)
                elif sutun_index == 5:  tablo.setColumnWidth(sutun_index, 120)
                else:                       tablo.setColumnWidth(sutun_index, 200) 
            
            elif tablo == rezTakip_ui.musteri_tableWidget:
                hucre = QTableWidgetItem(str(hucre_verisi))
                # Tabloya ekle
                tablo.setItem(satir_index, sutun_index, hucre)  
                tablo.setColumnWidth(sutun_index, 210) 
        
def uyari_ver(text,wait=3000):
    rezTakip_ui.statusbar.showMessage(str(text),wait)

def satir_sil_aktivite(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.aktivite_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                aktAdi = rezTakip_ui.aktivite_tableWidget.item(row, 0).text()
                print(aktAdi)
                curs.execute("DELETE FROM aktiviteler WHERE aktivite = ?", (aktAdi,))
                conn.commit()
                uyari_ver("Aktivite : {aktAdi} başarıyla silindi")
                sqlden_cagir_tabloya_dok(conn,curs,TABLO_AKTIVITELER,rezTakip_ui.aktivite_tableWidget)
    except:
        uyari_ver("! Aktivite Silme İşleminde hata oluştu !", 5000)

def sql_tablo_update_aktivite(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.aktivite_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                aktAdi =    rezTakip_ui.aktivite_tableWidget.item(row, 0).text()
                tl =        rezTakip_ui.aktivite_tableWidget.cellWidget(row,1).value()
                dolar =     rezTakip_ui.aktivite_tableWidget.cellWidget(row,2).value()
                euro =      rezTakip_ui.aktivite_tableWidget.cellWidget(row,3).value()
                kart =      rezTakip_ui.aktivite_tableWidget.cellWidget(row,4).value()
                print(aktAdi,tl,dolar,euro,kart)
                
                curs.execute(f"UPDATE {TABLO_AKTIVITELER} SET TL= ? , DOLAR = ?,EURO = ? , KART = ? WHERE aktivite = ?",
                    (tl,dolar,euro,kart,aktAdi))
                conn.commit()
                uyari_ver("Başarıyla güncellendi")

    except:
        uyari_ver("!! Beklenmeyen bir hata oluştu !!")

def satir_sil_rezervasyon(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.rezervasyon_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                rezID = rezTakip_ui.rezervasyon_tableWidget.item(row, 0).text()
                curs.execute("DELETE FROM rezervasyonlar WHERE rezID = ?", (rezID,))
                conn.commit()
                uyari_ver(f"Rezervasyon:{rezID} başarıyla silindi.")
                sqlden_cagir_tabloya_dok(conn,curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget)
    except:
        uyari_ver("! Masa Silme İşleminde hata oluştu !")

def sql_tablo_update_rezervasyon(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.aktivite_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                # id =                        rezTakip_ui.rezervasyon_tableWidget.item(row, 0).text()
                aktAdi =                    rezTakip_ui.rezervasyon_tableWidget.item(row, 1).text()
                otel_adi =                  rezTakip_ui.rezervasyon_tableWidget.item(row, 2).text()
                ad_soyad =                  rezTakip_ui.rezervasyon_tableWidget.item(row, 3).text()
                rezervasyon_tarihi =        rezTakip_ui.rezervasyon_tableWidget.item(row, 4).text()
                telefon =                   rezTakip_ui.rezervasyon_tableWidget.item(row, 5).text()
                # tutar =                     rezTakip_ui.rezervasyon_tableWidget.item(row, 6).text()
                # para_birimi=                rezTakip_ui.rezervasyon_tableWidget.item(row, 7).text()
                print(aktAdi,tl,dolar,euro,kart)
                
                curs.execute(f"UPDATE {TABLO_REZERVASYONLAR} SET TL= ? , DOLAR = ?,EURO = ? , KART = ? WHERE aktivite = ?",
                    (tl,dolar,euro,kart,aktAdi))
                conn.commit()
                uyari_ver("Başarıyla güncellendi")

    except:
        uyari_ver("!! Beklenmeyen bir hata oluştu !!")


def hucre_renklendir(tablo,row,column,color):
        item = tablo.item(row, column)
        if item:
            item.setBackground(color)

uyari_ver("asdasd",5000)


rezTakip()
rezTakip_ui.aktiviteListele_pushButton.click()
rezTakip_ui.musterilerListele_pushButton.click()
rezTakip_ui.rezervasyonListele_pushButton.click()
rezTakip_main_window.show()
sys.exit(Uygulama.exec_())