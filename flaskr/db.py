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

def heritage(db):
    query1 = """
    SELECT at.type_id, at.pourcentage FROM animaux_types at
    WHERE at.animal_id={0}
    """
    query2 = """
    SELECT av.velage_id, v.mere_id, v.pere_id FROM animaux_velages av, velages v
    WHERE av.animal_id={0} AND v.id=av.velage_id
    """
    def her(an):
        types = {i[0] : i[1] for i in db.execute(query1.format(an)).fetchall()}
        parents = db.execute(query2.format(an)).fetchall()
        if len(types) == 0:
            mere = her(parents[0][1])
            pere = her(parents[0][2])
            return {i : (mere.get(i, 0) + pere.get(i,0))/2 for i in list(set(mere.keys()) | set(pere.keys()))}
        return types

    for row in db.execute("SELECT id FROM animaux").fetchall():
        for item in her(row[0]).items():
            try:
                db.execute(f"INSERT INTO animaux_types (animal_id, type_id, pourcentage) VALUES ({row[0]},{item[0]},{item[1]});")
            except sqlite3.IntegrityError:
                pass

def init_db():
    db = get_db()
    with current_app.open_resource("data/schema.sql") as f:
        db.executescript(f.read().decode('utf8'))

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
    for file in sqlfiles:
        with current_app.open_resource("data/"+file) as f:
            for line in f.read().decode('utf8').split('\n'):
                try:
                    db.execute(line)
                except sqlite3.IntegrityError:
                    pass
    heritage(db)

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
