import sqlite3

conn = sqlite3.connect('Vaches.db')

cursor = conn.cursor()

for row in cursor.execute("SELECT id, famille_id, sexe, presence, apprivoise, mort_ne, decede from animaux"):
    print(row[0], "\t", row[1], "\t", row[2], "\t", row[3], "\t", row[4], "\t", row[5])
    break
conn.close()
