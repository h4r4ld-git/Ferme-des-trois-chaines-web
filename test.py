import sqlite3

conn = sqlite3.connect("Vaches.db")
cursor = conn.cursor()

def get_animals_types_counter():
    query = '''
        SELECT type, COUNT(*) AS amount
        FROM animaux_types
        LEFT JOIN types ON animaux_types.type_id = types.id
        GROUP BY type;
    '''

    return [data for data in cursor.execute(query)]

print(get_animals_types_counter())
