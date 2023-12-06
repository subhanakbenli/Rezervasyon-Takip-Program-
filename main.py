# sübhan akbenli    
import sqlite3
from PyQt5.QtWidgets import *
import sys
from datetime import datetime,timedelta
from ui_designs.rezTakip_ui import * 
from PyQt5.QtCore import QDate
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl import Workbook

TABLO_AKTIVITELER="aktiviteler"
INSERT_AKTIVITELER="(aktivite,TL,DOLAR,EURO,KART)"

TABLO_REZERVASYONLAR="rezervasyonlar"
INSERT_REZERVASYONLAR="(aktivite,otelAdi,adSoyad,rezDate,telefon,fiyat,paraBirimi)"

TABLO_MUSTERILER="musteriler"
INSERT_MUSTERILER="(otelAdi,telefon)"

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

class CustomComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore()
    
class CustomQDateEdit(QDateEdit):
    def wheelEvent(self, event):
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
                        (otelAdi Text PRIMARY KEY,telefon Text)")
        
        rezTakip_ui.aktiviteListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_AKTIVITELER,rezTakip_ui.aktivite_tableWidget))
        rezTakip_ui.rezervasyonListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget))
        rezTakip_ui.musterilerListele_pushButton.clicked.connect(lambda : 
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_MUSTERILER,rezTakip_ui.musteri_tableWidget) )
        
        rezTakip_ui.rezYap_pushButton.clicked.connect(lambda : 
            self.satir_ekle(rezTakip_ui.rezervasyon_tableWidget))
        rezTakip_ui.aktEkle_pushButton.clicked.connect(lambda : 
            self.satir_ekle(rezTakip_ui.aktivite_tableWidget))
        rezTakip_ui.musEkle_pushButton.clicked.connect(lambda :
            self.satir_ekle(rezTakip_ui.musteri_tableWidget))
        
        rezTakip_ui.oteldenRezGetir_pushButton.clicked.connect(lambda : rezervasyon_oteladi_SCTD(
                self.conn,self.curs,TABLO_REZERVASYONLAR,
                rezTakip_ui.rezervasyon_tableWidget,
                rezTakip_ui.musteri_tableWidget.item(rezTakip_ui.musteri_tableWidget.currentRow(),0).text())
                ) if rezTakip_ui.musteri_tableWidget.item(rezTakip_ui.musteri_tableWidget.currentRow(),0) is not None else Exception("Lütfen önce otel seçiniz")
    
        rezTakip_ui.aktivitedenRezGetir_pushButton.clicked.connect(lambda : rezervasyon_aktivite_SCTD(
                self.conn,self.curs,TABLO_REZERVASYONLAR,
                rezTakip_ui.rezervasyon_tableWidget,
                rezTakip_ui.aktivite_tableWidget.item(rezTakip_ui.aktivite_tableWidget.currentRow(),0).text())
                ) if rezTakip_ui.aktivite_tableWidget.item(rezTakip_ui.aktivite_tableWidget.currentRow(),0) is not None else Exception("Lütfen önce aktivite seçiniz")
        
        rezTakip_ui.UygunRezAra_pushButton.clicked.connect(lambda : rezervasyon_tarih_SCTD(
                self.conn,self.curs,TABLO_REZERVASYONLAR,
                rezTakip_ui.rezervasyon_tableWidget,
                rezTakip_ui.giris_dateEdit.date().toPyDate(),
                rezTakip_ui.cikis_dateEdit.date().toPyDate())
                )
        
    
        
        # rezTakip_ui.musteri_tableWidget.doubleClicked.connect(lambda :
    def satir_ekle(self, tablo):
        global otelAdi_rezervasyon_combo_data , aktivite_rezervasyon_combo_data
        row = tablo.rowCount() 
        son = tablo.columnCount() - 2
        # Check if the row index is within the valid range
        if row >= 0:
            # Check if the widget in the specified cell is None
            widget = tablo.cellWidget(row-1, son)

            if widget is not None and isinstance(widget, QPushButton) and widget.text() != "Kaydet":
                tablo.setRowCount(row + 1)
                v_scroll_bar = tablo.verticalScrollBar()
                v_scroll_bar.setValue(v_scroll_bar.maximum())
                save_button = QPushButton("Kaydet")
                save_button.setStyleSheet("background-color: rgb(105,255,105)")
                save_button.setMaximumWidth(125)        
                tablo.setCellWidget(row, son, save_button)
                
                # Make sure to connect the correct method to the button click event
                if tablo == rezTakip_ui.aktivite_tableWidget:
                    save_button.clicked.connect(lambda: self.aktivite_kaydet())
                elif tablo == rezTakip_ui.rezervasyon_tableWidget:
                    save_button.clicked.connect(lambda: self.rezervasyon_kaydet())
                    
                    aktivite_combo=CustomComboBox()
                    aktivite_combo.addItem("--")
                    aktivite_combo.addItems(aktivite_rezervasyon_combo_data)                    
                    aktivite_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")   
                    tablo.setCellWidget(row, 1, aktivite_combo)
                    
                    otelAdi_combo=CustomComboBox()
                    otelAdi_combo.addItem("--")
                    otelAdi_combo.addItems(otelAdi_rezervasyon_combo_data)   
                    otelAdi_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    tablo.setCellWidget(row , 2, otelAdi_combo)
                    
                    date_edit=CustomQDateEdit()
                    date_edit.setDate(datetime.today().date())
                    date_edit.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    tablo.setCellWidget(row , 4,date_edit)
                    
                    
                    birim_combo=CustomComboBox()
                    birim_combo.addItems(["TL","DOLAR","EURO","KART"])  
                    birim_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    
                    tablo.setCellWidget(row , 7,birim_combo)
                    
                elif tablo == rezTakip_ui.musteri_tableWidget:
                    save_button.clicked.connect(lambda: self.musteri_kaydet())
            else:
                uyari_ver("Lütfen önceki satırı kaydediniz", 5000)
        else:
            uyari_ver("Geçerli bir satır indeksi bulunamadı", 5000)

    def aktivite_kaydet(self):    
        try:
            row = rezTakip_ui.aktivite_tableWidget.rowCount() - 1
            try:
                aktivite = rezTakip_ui.aktivite_tableWidget.item(row, 0).text()
            except:
                raise Exception("Aktivite adı boş bırakılamaz")
            try:
                tl = rezTakip_ui.aktivite_tableWidget.item(row, 1).text()
            except:
                tl=0
            try:
                dolar = rezTakip_ui.aktivite_tableWidget.item(row, 2).text()
            except:
                dolar=0
            try:
                euro = rezTakip_ui.aktivite_tableWidget.item(row, 3).text()
            except:
                euro=0
            try:    
                kart = rezTakip_ui.aktivite_tableWidget.item(row, 4).text()
            except:     
                kart=0
            print(aktivite,tl,dolar,euro,kart)
            sql_tabloya_ekle(self.conn,self.curs, TABLO_AKTIVITELER, (aktivite,tl,dolar,euro,kart))
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_AKTIVITELER,rezTakip_ui.aktivite_tableWidget)
        except Exception as e:
            uyari_ver(str(e))

    def rezervasyon_kaydet(self):
        try:
            row = rezTakip_ui.rezervasyon_tableWidget.rowCount() - 1
            try:
                aktivite = rezTakip_ui.rezervasyon_tableWidget.cellWidget(row, 1).currentText()
            except:
                aktivite="--"
            try:
                otel_adi = rezTakip_ui.rezervasyon_tableWidget.cellWidget(row, 2).currentText()
            except:
                otel_adi="--"
            try:
                ad_soyad = rezTakip_ui.rezervasyon_tableWidget.item(row, 3).text()
            except:
                ad_soyad="--"
            try:
                rezervasyon_tarihi = rezTakip_ui.rezervasyon_tableWidget.cellWidget(row , 4).date().toPyDate()
            except:
                rezervasyon_tarihi=datetime.today().date()
            try:
                telefon = rezTakip_ui.rezervasyon_tableWidget.item(row, 5).text()
            except:
                telefon="--"
            para_birimi=rezTakip_ui.rezervasyon_tableWidget.cellWidget(row,7).currentText()
            self.curs.execute(f"SELECT {para_birimi} FROM {TABLO_AKTIVITELER} where  aktivite = ?",(aktivite,))
            fiyat= self.curs.fetchone()
            if fiyat != None:
                fiyat=fiyat[0]
                sql_tabloya_ekle(self.conn,self.curs, f"{TABLO_REZERVASYONLAR} {INSERT_REZERVASYONLAR}", (aktivite,otel_adi,ad_soyad,rezervasyon_tarihi,telefon,fiyat,para_birimi))
                sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget)
            else:
                uyari_ver("Bu aktivite için fiyat bulunamadı !!")
                return
            print(aktivite,otel_adi,ad_soyad,rezervasyon_tarihi,telefon,para_birimi)
        except:
            uyari_ver("!! Beklenmeyen bir hata oluştu -rezervasyon_kaydet-!!")  

    def musteri_kaydet(self):    
        try:
            row=rezTakip_ui.musteri_tableWidget.rowCount() - 1
            otel_adi = rezTakip_ui.musteri_tableWidget.item(row, 0).text()
            try:
                telefon = rezTakip_ui.musteri_tableWidget.item(row, 1).text()
            except:
                telefon="00000000000"
                
            sql_tabloya_ekle(self.conn,self.curs, f"{TABLO_MUSTERILER} {INSERT_MUSTERILER}", (otel_adi,telefon))
            sqlden_cagir_tabloya_dok(self.conn,self.curs,TABLO_MUSTERILER,rezTakip_ui.musteri_tableWidget)
            
        except:
            uyari_ver("!! Beklenmeyen bir hata oluştu -musteri_kaydet-!!")


def tabloya_dok(conn,curs,tablo, satirlar):
    """
    Tabloya verilen satırları ekleyen fonksiyon.

    :param tablo: QTableWidget nesnesi
    :param satirlar: Liste içinde satırlar. Her bir satır da bir liste olmalıdır.
    """
    global otelAdi_rezervasyon_combo_data , aktivite_rezervasyon_combo_data
    
    curs.execute(f"SELECT aktivite FROM {TABLO_AKTIVITELER}")
    aktivite_rezervasyon_combo_data=[i[0] for i in curs.fetchall()]
    curs.execute(f"SELECT otelAdi FROM {TABLO_MUSTERILER}")
    otelAdi_rezervasyon_combo_data=[i[0] for i in curs.fetchall()]
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
            rezTakip_ui.tabWidget.setCurrentIndex(0)      
        elif tablo == rezTakip_ui.rezervasyon_tableWidget:  
            update_button.clicked.connect(lambda : sql_tablo_update_rezervasyon(conn,curs))
            delete_button.clicked.connect(lambda : satir_sil_rezervasyon(conn,curs))
            rezTakip_ui.tabWidget.setCurrentIndex(1)
        elif tablo == rezTakip_ui.musteri_tableWidget:  
            update_button.clicked.connect(lambda : sql_tablo_update_musteri(conn,curs))
            delete_button.clicked.connect(lambda : satir_sil_musteri(conn,curs))
            rezTakip_ui.tabWidget.setCurrentIndex(2)
        # Her bir hücreyi eklemek için döngü        
        for sutun_index, hucre_verisi in enumerate(satir):
             
            if tablo == rezTakip_ui.aktivite_tableWidget:         
                    
                if sutun_index==0:          
                    hucre = QTableWidgetItem(str(hucre_verisi))
                    tablo.setItem(satir_index, sutun_index, hucre)                      
                    tablo.setColumnWidth(sutun_index, 450)
                    tablo.item(satir_index, sutun_index).setFlags(tablo.item(satir_index, sutun_index).flags() ^ 2) ### burayı incele
                    
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
                    tablo.item(satir_index, sutun_index).setFlags(tablo.item(satir_index, sutun_index).flags() ^ 2) ### burayı incele
                elif sutun_index ==1:
                    aktivite_combo=CustomComboBox()
                    aktivite_combo.addItem("--")
                    aktivite_combo.addItems(aktivite_rezervasyon_combo_data)
                    aktivite_combo.setCurrentText(hucre_verisi)
                    
                    aktivite_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")   
                    tablo.setCellWidget(satir_index, sutun_index, aktivite_combo)
                    tablo.setColumnWidth(sutun_index, 200)
                    
                elif sutun_index ==2:
                    otelAdi_combo=CustomComboBox()
                    otelAdi_combo.addItem("--")
                    otelAdi_combo.addItems(otelAdi_rezervasyon_combo_data)
                    otelAdi_combo.setCurrentText(hucre_verisi)
                    
                    otelAdi_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    tablo.setCellWidget(satir_index, sutun_index, otelAdi_combo)
                    tablo.setColumnWidth(sutun_index, 200)
                elif sutun_index == 4 :     
                    date_edit=CustomQDateEdit()
                    tarih=QDate.fromString(hucre_verisi, "yyyy-MM-dd")
                    date_edit.setDate(tarih)
                    date_edit.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    tablo.setCellWidget(satir_index, sutun_index,date_edit)
                    tablo.setColumnWidth(sutun_index, 150)
                    
                elif sutun_index == 5:  
                    tablo.setColumnWidth(sutun_index, 160)  
                                  
                elif sutun_index==6:          
                    tablo.setColumnWidth(sutun_index, 105)
                    tablo.item(satir_index, sutun_index).setFlags(tablo.item(satir_index, sutun_index).flags() ^ 2) ### burayı incele

                elif sutun_index==7:        
                    birim_combo=CustomComboBox()
                    birim_combo.addItems(["TL","DOLAR","EURO","KART"])  
                    birim_combo.setCurrentText(hucre_verisi)
                    birim_combo.setStyleSheet("background-color : rgb(235,235,235); font-size : 18px; font-family : Times New Roman")
                    
                    tablo.setCellWidget(satir_index, sutun_index,birim_combo)
                    tablo.setColumnWidth(sutun_index, 120)

                else:                       tablo.setColumnWidth(sutun_index, 200) 
        
            elif tablo == rezTakip_ui.musteri_tableWidget:
                hucre = QTableWidgetItem(str(hucre_verisi))
                tablo.setItem(satir_index, sutun_index, hucre)  

                if sutun_index==0:
                    
                    tablo.setColumnWidth(sutun_index, 250) 
                    tablo.item(satir_index, sutun_index).setFlags(tablo.item(satir_index, sutun_index).flags() ^ 2) ### burayı incele
                    birimler=["TL","DOLAR","EURO","KART"]
                    for add,birim in enumerate(birimler): # burada otelin ödemesi gerek toplam fiyatı yazıyoruz
                        total=fiyatlari_topla(conn,curs,str(hucre_verisi),birim)
                        hucre = QTableWidgetItem(str(total))
                        tablo.setItem(satir_index, 2+add, hucre)  
                        tablo.setColumnWidth(2+add, 200)
                        tablo.item(satir_index, 2+add).setFlags(tablo.item(satir_index, 2+add).flags() ^ 2) ### burayı incele
                elif 1<sutun_index<5:
                    tablo.setColumnWidth(sutun_index, 200) 
                    tablo.item(satir_index, sutun_index).setFlags(tablo.item(satir_index, sutun_index).flags() ^ 2) ### burayı incele
                    
                else: 
                    tablo.setColumnWidth(sutun_index, 150)
   
      
def fiyatlari_topla(conn,curs,otel_adi,para_birimi):
    sql_sorgusu = """
    SELECT SUM(fiyat) AS toplamFiyat
    FROM rezervasyonlar
    WHERE otelAdi = ? AND paraBirimi = ?
    GROUP BY otelAdi, paraBirimi
    """
    # Sorguyu çalıştır
    curs.execute(sql_sorgusu, (otel_adi, para_birimi))
    toplam_fiyat=0
    # Sonuçları al
    sonuclar = curs.fetchall()
    for sonuc, in sonuclar:
        toplam_fiyat = sonuc  
    return toplam_fiyat
    # Veritabanı bağlantısını kapat
    
def sql_tabloya_ekle(conn,curs,tabloadi,veri):
    try:
        soru_isareti_sayisi=(len(veri)*'?,').strip(",")
        curs.execute(f"INSERT INTO {tabloadi} VALUES({soru_isareti_sayisi})",(veri))
        conn.commit()
        uyari_ver("Başarıyla eklendi")
    except    sqlite3.IntegrityError:
        uyari_ver("Bu otel adı daha önceden eklendi",5000)
    except Exception as e:
        uyari_ver(str(e),5000)


def rezervasyon_oteladi_SCTD(conn,curs,tablo_adi,tablo,otelAdi):
        curs.execute(f"SELECT * FROM {tablo_adi} WHERE otelAdi = ?",(otelAdi,))
        data=curs.fetchall()
        tabloya_dok(conn,curs,tablo,data)

def rezervasyon_tarih_SCTD(conn,curs,tablo_adi,tablo,baslangic_tarihi,bitis_tarihi):
        curs.execute(f"SELECT * FROM {tablo_adi} WHERE rezDate BETWEEN ? AND ?",(baslangic_tarihi,bitis_tarihi))
        data=curs.fetchall()
        tabloya_dok(conn,curs,tablo,data)

def rezervasyon_aktivite_SCTD(conn,curs,tablo_adi,tablo,aktivite):
        curs.execute(f"SELECT * FROM {tablo_adi} WHERE aktivite = ?",(aktivite,))
        data=curs.fetchall()
        tabloya_dok(conn,curs,tablo,data) 

def sqlden_cagir_tabloya_dok(conn,curs,tablo_adi,tablo):
        curs.execute(f"SELECT * FROM {tablo_adi}")
        data=curs.fetchall()
        tabloya_dok(conn,curs,tablo,data)
      
                          
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
                curs.execute(f"DELETE FROM {TABLO_AKTIVITELER} WHERE aktivite = ?", (aktAdi,))
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
                curs.execute(f"DELETE FROM {TABLO_REZERVASYONLAR} WHERE rezID = ?", (rezID,))
                conn.commit()
                uyari_ver(f"Rezervasyon:{rezID} başarıyla silindi.")
                sqlden_cagir_tabloya_dok(conn,curs,TABLO_REZERVASYONLAR,rezTakip_ui.rezervasyon_tableWidget)
    except:
        uyari_ver("! Rezervasyon Silme İşleminde hata oluştu !")

def sql_tablo_update_rezervasyon(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.rezervasyon_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                id =                        rezTakip_ui.rezervasyon_tableWidget.item(row, 0).text()
                aktAdi =                    rezTakip_ui.rezervasyon_tableWidget.cellWidget(row, 1).currentText()
                otel_adi =                  rezTakip_ui.rezervasyon_tableWidget.cellWidget(row, 2).currentText()
                ad_soyad =                  rezTakip_ui.rezervasyon_tableWidget.item(row, 3).text()
                rezervasyon_tarihi =        rezTakip_ui.rezervasyon_tableWidget.cellWidget(row , 4).date().toPyDate()
                telefon =                   rezTakip_ui.rezervasyon_tableWidget.item(row, 5).text()
                para_birimi=                rezTakip_ui.rezervasyon_tableWidget.cellWidget(row,7).currentText()
                curs.execute(f"SELECT {para_birimi} FROM {TABLO_AKTIVITELER} where  aktivite = ?",(aktAdi,))
                fiyat= curs.fetchone()
                
                if fiyat != None:
                    fiyat=fiyat[0]    
                    curs.execute(f"UPDATE {TABLO_REZERVASYONLAR} SET aktivite = ?,otelAdi = ?,adSoyad = ?,rezDate =?,telefon = ?,fiyat = ?,paraBirimi=? WHERE rezID = ?",
                        (aktAdi,otel_adi,ad_soyad,rezervasyon_tarihi,telefon,fiyat,para_birimi,        id))
                    conn.commit()
                    uyari_ver("Başarıyla güncellendi")
                    rezTakip_ui.rezervasyon_tableWidget.setItem(row, 6, QTableWidgetItem(str(fiyat)))
                else:
                    uyari_ver("Bu aktivite için fiyat bulunamadı !!")

    except:
        uyari_ver("!! Beklenmeyen bir hata oluştu !!")


def satir_sil_musteri(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.musteri_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                otelAdi = rezTakip_ui.musteri_tableWidget.item(row, 0).text()
                curs.execute(f"DELETE FROM {TABLO_MUSTERILER} WHERE otelAdi = ?", (otelAdi,))
                conn.commit()
                uyari_ver(f"Rezervasyon:{otelAdi} başarıyla silindi.")
                sqlden_cagir_tabloya_dok(conn,curs,TABLO_MUSTERILER,rezTakip_ui.musteri_tableWidget)
    except:
        uyari_ver("! Otel Silme İşleminde hata oluştu !")

def sql_tablo_update_musteri(conn,curs):
    try: 
        sender_button = rezTakip_main_window.sender()
        if sender_button:
            index = rezTakip_ui.rezervasyon_tableWidget.indexAt(sender_button.pos())
            
            if index.isValid():
                row = index.row()
                otel_adi =                  rezTakip_ui.rezervasyon_tableWidget.item(row, 0).text()
                telefon =                   rezTakip_ui.rezervasyon_tableWidget.item(row, 1).text()
                curs.execute(f"UPDATE {TABLO_MUSTERILER} SET telefon = ? WHERE otelAdi = ?",
                        (telefon,otel_adi))
                conn.commit()
                uyari_ver("Başarıyla güncellendi")

    except:
        uyari_ver("!! Beklenmeyen bir hata oluştu !!")


def hucre_renklendir(tablo,row,column,color):
        item = tablo.item(row, column)
        if item:
            item.setBackground(color)

def tabloları_excel_aktar():
    # try:
        aktivite_liste=[[rezTakip_ui.aktivite_tableWidget.horizontalHeaderItem(i).text() for i in range(rezTakip_ui.aktivite_tableWidget.columnCount()-2)]]
        for satir in range(rezTakip_ui.aktivite_tableWidget.rowCount()):
            satir_liste=[]
            for sutun in range(rezTakip_ui.aktivite_tableWidget.columnCount()-2):
                if sutun==0:
                    satir_liste.append(rezTakip_ui.aktivite_tableWidget.item(satir,sutun).text())
                else:
                    satir_liste.append(rezTakip_ui.aktivite_tableWidget.cellWidget(satir,sutun).value())
            aktivite_liste.append(satir_liste)
        
        rezervasyon_liste=[[rezTakip_ui.rezervasyon_tableWidget.horizontalHeaderItem(i).text() for i in range(rezTakip_ui.rezervasyon_tableWidget.columnCount()-2)]]
        for satir in range(rezTakip_ui.rezervasyon_tableWidget.rowCount()):
            satir_liste=[]
            for sutun in range(rezTakip_ui.rezervasyon_tableWidget.columnCount()-2):
                
                if sutun==4:
                    satir_liste.append(rezTakip_ui.rezervasyon_tableWidget.cellWidget(satir,sutun).date().toPyDate())
                elif sutun ==1 or sutun==2 or sutun==7:
                    satir_liste.append(rezTakip_ui.rezervasyon_tableWidget.cellWidget(satir,sutun).currentText())
                elif sutun==0 or sutun==3 or sutun==5 or sutun==6:
                    satir_liste.append(rezTakip_ui.rezervasyon_tableWidget.item(satir,sutun).text())
                else:
                    satir_liste.append(rezTakip_ui.rezervasyon_tableWidget.cellWidget(satir,sutun).currentText())
            rezervasyon_liste.append(satir_liste)
        
        musteri_liste=[]
        for satir in range(rezTakip_ui.musteri_tableWidget.rowCount()):
            satir_liste=[]
            for sutun in range(rezTakip_ui.musteri_tableWidget.columnCount()-2):
                satir_liste.append(rezTakip_ui.musteri_tableWidget.item(satir,sutun).text())
            musteri_liste.append(satir_liste)
        excele_yaz([aktivite_liste,rezervasyon_liste,musteri_liste],"Output")
    # except Exception as e:
    #     uyari_ver(str(e),5000)


# Arka plan rengini ayarlamak için doldurma nesnesi oluştur
fillSari = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')  # Burada sarı renk seçildi
fillYesil = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')  # Burada yeşil renk seçildi
fillKirmizi = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')  # Burada kırmızı renk seçildi
fillMavi = PatternFill(start_color='66CCFF', end_color='66CCFF', fill_type='solid')  # Burada mavi renk seçildi
def excele_yaz(liste,dosyaAdi):
    workbook = Workbook()
    for index,sayfa in enumerate(liste):
        sayfa_adi = "Aktiviteler" if index==0 else "Rezervasyonlar" if index==1 else "Müşteriler"
        sheet = workbook.create_sheet("output",index)
        row=1
        sayac = 0
        for satir in sayfa:
            sutunList=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            sutunsayisi=len(satir)
            for sutunIndeks in range(sutunsayisi):
                sheet.column_dimensions[sutunList[sutunIndeks]].width = 20  # sütun için genişlik 20
            if sayac==0: # burada yazılan satır başlık satırı ise font ve renk ayarlıyoruz
                font = Font(size=13,bold=True)  # 14 punto metin boyutu
                fill=fillMavi
            else:
                font = Font(size=10)
                fill=fillSari
            for cell,col in zip(satir,sutunList):
                sheet[f'{col}{row}'] = f'{cell}'
                sheet[f'{col}{row}'].fill= fill
                sheet[f'{col}{row}'].font = font
            row+=1
            sayac+=1


    try:

        workbook.save(f'{dosyaAdi}.xlsx')
    except: 
        print("Excel Dosyasını kapatınız")


rezTakip_ui.giris_dateEdit.setDate(datetime.today().date())
rezTakip_ui.cikis_dateEdit.setDate(datetime.today().date()+timedelta(days=1))
rezTakip_ui.giris_dateEdit.setCalendarPopup(True)
rezTakip_ui.cikis_dateEdit.setCalendarPopup(True)
try:
    sınıf=rezTakip()
except Exception as e:
    uyari_ver(str(e),5000)

rezTakip_ui.aktiviteListele_pushButton.click()
rezTakip_ui.musterilerListele_pushButton.click()
rezTakip_ui.rezervasyonListele_pushButton.click()
rezTakip_main_window.show()
tabloları_excel_aktar()

sys.exit(Uygulama.exec_())