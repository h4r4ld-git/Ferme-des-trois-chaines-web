import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')

def index():
    """
    retourne le contenu de la page index.html
    """
    conn = sqlite3.connect('Vaches.db')
    cursor = conn.cursor()
    mnth = []
    for row in cursor.execute("SELECT date from velages"):
        if row[0].split("/")[1:] == ["10","2020"]:
            mnth.append(row[0])

    freq = []
    for i in range(1,29):
        date = str(i) + "/10/2020"
        if i < 10:
            date = "0" + date

        if date in mnth:
            freq.append(mnth.count(date))
        else:
            freq.append(0)

    mort_nids = []
    freq1 = [0 for i in range(12)]
    for row in cursor.execute("SELECT id from animaux where mort_ne=1"):
        mort_nids.append(row[0])
    for i in mort_nids:
        for row in cursor.execute(f"SELECT date from velages where id={i}"):
            if row[0].split("/")[2] == "2020":
                freq1[int(row[0].split("/")[1])-1] += 1

    conn.close()
    return render_template("index.html", jours = [i for i in range(1,29)], freq = freq, freq1 = freq1)

if __name__ == "__main__":
    app.run()
