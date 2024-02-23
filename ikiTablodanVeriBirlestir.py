import sqlite3

# SQLite veritabanına bağlan
conn = sqlite3.connect('veritabani.db')
cursor = conn.cursor()

# Örnek tabloları oluştur
cursor.execute('''CREATE TABLE IF NOT EXISTS table1
                  (id INTEGER PRIMARY KEY, tutar INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS table2
                  (id INTEGER, tutar INTEGER)''')

# Örnek verileri ekle
cursor.execute("INSERT INTO table1 VALUES (1, 100)")
cursor.execute("INSERT INTO table1 VALUES (2, 150)")

cursor.execute("INSERT INTO table2 VALUES (1, 200)")
cursor.execute("INSERT INTO table2 VALUES (1, 50)")
cursor.execute("INSERT INTO table2 VALUES (2, 75)")

# İki tablodan idsi aynı olan satırların tutar kısmını topla
cursor.execute('''SELECT id, SUM(tutar) AS toplam_tutar
                  FROM (
                      SELECT id, tutar FROM table1
                      UNION ALL
                      SELECT id, tutar FROM table2
                  ) AS combined
                  GROUP BY id''')

# Sonuçları al
results = cursor.fetchall()

# Sonuçları yazdır
for row in results:
    print(f"ID: {row[0]}, Toplam Tutar: {row[1]}")

# Bağlantıyı kapat
conn.close()