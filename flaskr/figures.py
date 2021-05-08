import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.db import get_db

bp = Blueprint('Figures', __name__, url_prefix='/')

@bp.route('/',methods=['GET', 'POST'])
def figures():
    db = get_db()
    query = """
    SELECT SUBSTR(v.date,1,2) FROM velages v
    """
    ex_query = db.execute(query).fetchall()
    data = {int(i[0]):ex_query.count(i) for i in ex_query}

    query1 = """
    SELECT SUBSTR(v.date,4,2) FROM animaux a, velages v, animaux_velages av WHERE a.mort_ne=1 AND av.animal_id=a.id AND av.velage_id=v.id
    """
    ex_query = db.execute(query1).fetchall()
    data1 = {int(i[0]):ex_query.count(i) for i in ex_query}

    query = """
    SELECT id, nom FROM familles
    """
    decedes = """
    SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=1
    """
    vivants = """
    SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=0
    """
    familles = db.execute(query).fetchall()
    proportions = {i[1]:(db.execute(decedes.format(i[0])).fetchall()[0][0]/db.execute(vivants.format(i[0])).fetchall()[0][0])*100 for i in familles}


    return render_template("base.html", f1 = [[i for i in range(1,29)],[data.get(i,0)/20 for i in range(1,29)]], f2 = [data1.get(i,0)/20 for i in range(1,13)], f3 = [proportions.keys(), list(proportions.values())])
