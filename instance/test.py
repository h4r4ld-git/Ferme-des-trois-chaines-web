import sqlite3

conn = sqlite3.connect("flaskr.sqlite")
cursor = conn.cursor()
query = """
SELECT id, nom FROM familles
"""
decedes = """
SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=1
"""
vivants = """
SELECT COUNT(*) FROM animaux a WHERE a.famille_id={0} AND a.decede=0
"""
familles = cursor.execute(query).fetchall()
proportions = {i[1]:(cursor.execute(decedes.format(i[0])).fetchall()[0][0]/cursor.execute(vivants.format(i[0])).fetchall()[0][0])*100 for i in familles}

print(proportions)
conn.close()


"""
def get_animals_types_counter():
    query = '''
        SELECT type, COUNT(*) AS amount
        FROM animaux_types
        LEFT JOIN types ON animaux_types.type_id = types.id
        GROUP BY type;
    '''

    return [data for data in cursor.execute(query)]
"""
#print(get_animals_types_counter())
