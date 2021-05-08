import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def heritage():
    """
    Pre : -
    Post : Ajoute l'heritage genetique de chaque animal dans la table 'animaux_types' de la base données (Si il n'existe pas)
    """
    db = get_db()
    # Type et pourcentage pour l'animal
    query1 = """
    SELECT at.type_id, at.pourcentage FROM animaux_types at
    WHERE at.animal_id={0}
    """
    # velage-id, pere et mere de l'animal
    query2 = """
    SELECT av.velage_id, v.mere_id, v.pere_id FROM animaux_velages av, velages v
    WHERE av.animal_id={0} AND v.id=av.velage_id
    """
    def her(an):
        """
        Pre : 'an' est un id dans la table 'animaux'
        Post : retourne un dictionnaire en format {type : pourcentage} pour l'animal 'an'
        """
        types = {i[0] : i[1] for i in db.execute(query1.format(an)).fetchall()} # Dictionnaire en format {type: pourcentage} pour l'animal 'an'
        parents = db.execute(query2.format(an)).fetchall() # Parents de l'animal
        if len(types) == 0: # Si il n'y a pas de types pour l'animal
            mere = her(parents[0][1]) # l'heritage de la mere
            pere = her(parents[0][2]) # l'heritage du pere
            return {i : (mere.get(i, 0) + pere.get(i,0))/2 for i in list(set(mere.keys()) | set(pere.keys()))} # Dictionnaire en format {type: la somme des pourcentages du type des parents diviser par deux}
        return types

    for row in db.execute("SELECT id FROM animaux").fetchall(): # Pour chaque animal
        for item in her(row[0]).items(): # Pour chaque type et pourcentage de l'animal
            try:
                db.execute(f"INSERT INTO animaux_types (animal_id, type_id, pourcentage) VALUES ({row[0]},{item[0]},{item[1]});") # Inserer l'heritage genetique
            except sqlite3.IntegrityError:
                pass

def get_type_quantite():
    db = get_db()
    # Nombre d'animal pour chaque type
    query = """
    SELECT type, COUNT(*) FROM animaux_types
    LEFT JOIN types ON animaux_types.type_id = types.id
    GROUP BY type
    """
    return [(i[0], i[1]) for i in db.execute(query).fetchall()]

def init_db():
    db = get_db()
    # Creer le schema de la base
    with current_app.open_resource("data/schema.sql") as f:
        db.executescript(f.read().decode('utf8'))

    # Fichiers des données sql
    sqlfiles = [
        "insert_animaux_types.sql",
        "insert_animaux.sql",
        "insert_animaux_velages.sql",
        "insert_complications.sql",
        "insert_familles.sql",
        "insert_types.sql",
        "insert_velages_complications.sql",
        "insert_velages.sql"
    ]

    # Inserer les données dans la base
    for file in sqlfiles:
        with current_app.open_resource("data/"+file) as f:
            for line in f.read().decode('utf8').split('\n'):
                try:
                    db.execute(line)
                except sqlite3.IntegrityError:
                    pass
    # Inserer les heritages de chaque animal dans la base
    heritage()

    db.commit() # Enregistrer les modifications


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
