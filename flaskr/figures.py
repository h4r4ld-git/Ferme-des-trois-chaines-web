import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.db import get_db

bp = Blueprint('Figures', __name__, url_prefix='/')

def figure1_data():
    db = get_db()
    query = """
    SELECT SUBSTR(v.date,1,2), CAST(COUNT(*) AS float)/30.0 FROM velages v
    GROUP BY SUBSTR(v.date,1,2)
    """
    ex_query = db.execute(query).fetchall() # [(Jours de naissances, nombre de naissance en moyenne)]
    return [[i[0] for i in ex_query[:-3]],[i[1] for i in ex_query[:-3]]] # [[1-28], [nombres des naissances de 1991 à 2020 dans l'ordre selon les jours, divisé par 30]]


def figure2_data():
    db = get_db()
    query1 = """
    SELECT SUBSTR(v.date,4,2), CAST(COUNT(*) AS float)/30.0 FROM animaux a, velages v, animaux_velages av WHERE a.mort_ne=1 AND av.animal_id=a.id AND av.velage_id=v.id
    GROUP BY SUBSTR(v.date,4,2)
    """
    ex_query = db.execute(query1).fetchall() # [(mois, nombre de mort_nés)]
    return [i[1] for i in ex_query] # [Nombres de mort_nés de 1991 et 2020 dans l'ordre selon les mois, divisé par 30]

def figure3_data():
    db = get_db()
    # requetes SQL
    noms_proportions = """
    SELECT nom, (SELECT CAST(COUNT(*) AS float) FROM animaux a WHERE a.famille_id=familles.id AND a.decede=1)/(SELECT CAST(COUNT(*) AS float) FROM animaux a WHERE a.famille_id=familles.id AND a.decede=0)*100
    FROM animaux a
    LEFT JOIN familles ON a.famille_id=familles.id
    GROUP BY nom
    """
    ex_query = db.execute(noms_proportions).fetchall()
    return [[i[0] for i in ex_query],[i[1] for i in ex_query]] # [noms des familles, les proportions]

@bp.route('/',methods=['GET', 'POST'])
def figures():
    db = get_db() # Connexion à la base de données

    # Passer les données à 'base.html' et afficher
    return render_template("base.html", f1 = figure1_data(), f2 = figure2_data(), f3 = figure3_data())
