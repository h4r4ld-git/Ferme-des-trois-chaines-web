import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.db import get_db

bp = Blueprint('Figures', __name__, url_prefix='/')

@bp.route('/',methods=['GET', 'POST'])
def figures():
    db = get_db()
    # Figure 1
    query = """
    SELECT SUBSTR(v.date,1,2) FROM velages v
    """
    ex_query = db.execute(query).fetchall() # Jours de naissances
    data = {int(i[0]):ex_query.count(i) for i in ex_query} # Dictionnaire en format {jour de naissance: nombre de naissances}

    # Figure 2
    query1 = """
    SELECT SUBSTR(v.date,4,2) FROM animaux a, velages v, animaux_velages av WHERE a.mort_ne=1 AND av.animal_id=a.id AND av.velage_id=v.id
    """
    ex_query = db.execute(query1).fetchall() # Les mois de naissances des mort_nés
    data1 = {int(i[0]):ex_query.count(i) for i in ex_query} # Dictionnaire en format {mois de naissance: nombre de mort_nés}

    # Figure 3
    query = """
    SELECT id, nom FROM familles
    """
    decedes = """
    SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=1
    """
    vivants = """
    SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=0
    """
    familles = db.execute(query).fetchall() # ID de chaque famille
    proportions = {i[1]:(db.execute(decedes.format(i[0])).fetchall()[0][0]/db.execute(vivants.format(i[0])).fetchall()[0][0])*100 for i in familles} # Dictionnaire en format {nom de famille: rapport entre décés et vivants pour cette famille}

    # Passer les données à 'base.html' et afficher
    return render_template("base.html", f1 = [[i for i in range(1,29)],[data.get(i,0)/20 for i in range(1,29)]], f2 = [data1.get(i,0)/20 for i in range(1,13)], f3 = [proportions.keys(), list(proportions.values())])
