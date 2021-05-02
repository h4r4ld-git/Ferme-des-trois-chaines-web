import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    retourne le contenu de la page index.html
    """
    # Connection sur la base de données
    conn = sqlite3.connect('Vaches.db')
    cursor = conn.cursor()

    # Figure 1
    mnth = [] # Liste des dates de velage du 10/2020
    for row in cursor.execute("SELECT date from velages"):
        if row[0].split("/")[1:] == ["10","2020"]:
            mnth.append(row[0])

    freq = [] # Liste de nombre de naissances dans le meme ordre que les dates dans 'mnth'
    for i in range(1,29): # Compter les naissances pour 28 jours
        date = str(i) + "/10/2020"
        if i < 10:
            date = "0" + date
        if date in mnth:
            freq.append(mnth.count(date)) # Ajouter le nombre de date dans 'mnth'
        else:
            freq.append(0) # La date n'est pas dans la liste

    # Figure 2
    mort_nids = [] # Les ID des animaux mort-né
    freq1 = [0 for i in range(12)] # Liste de nombre de mort-né pour chaque mois dans l'ordre
    for row in cursor.execute("SELECT id from animaux where mort_ne=1"):
        mort_nids.append(row[0])
    for i in mort_nids: # Pour chaque mort-né
        for row in cursor.execute(f"SELECT date from velages where id={i}"):
            dt = row[0].split("/") # [jour, mois, année]
            if dt[2] == "2020":
                freq1[int(dt[1])-1] += 1

    # Figure 3
    familles = {} # dictionnaire en format {'famille id' : ([0,0], 'nom de famille')} pour chaque famille
    for row in cursor.execute("SELECT nom, id from familles"):
        familles[row[1]] = ([0,0],row[0])

    for row in cursor.execute("SELECT * from animaux"):
        if row[-1]: # décédé prématurement: 0 ou 1
            familles[row[1]][0][0] -= 1 # Si décédé décrementer [-1,0]
        else:
            familles[row[1]][0][1] += 1 # Si vivant incrementer [0,1]
    ndfamille = [i[1][1] for i in familles.items()] # Liste des noms de familles dans l'ordre
    dcfamille = [i[1][0][0] for i in familles.items()] # Liste des nombres de décédés dans l'ordre
    vvfamille = [i[1][0][1] for i in familles.items()] # Liste des nombres de vivants dans l'ordre
    conn.close() # Terminer la connection
    # render_template va chercher index.html dans templates en passant les arguments qui seront utiles pour les figures
    return render_template("index.html", jours = [i for i in range(1,29)], freq = freq, freq1 = freq1, nd = ndfamille, dc = dcfamille, vv = vvfamille)

if __name__ == "__main__":
    app.run() # Lancer le site
