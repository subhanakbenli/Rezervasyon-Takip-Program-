from PyQt5 import uic

with open('ui_designs/anaekranUI.py', 'w', encoding='utf-8') as fout:       uic.compileUi('ui_designs/anaekran.ui',fout)
with open('ui_designs/odaaramaUI.py', 'w', encoding='utf-8') as fout:       uic.compileUi('ui_designs/OdaAramaUI.ui',fout)
