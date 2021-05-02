import sqlite3

conn = sqlite3.connect('Vaches.db')

cursor = conn.cursor()

def heritage_genetique(parent):
    a_types = []
    for row in cursor.execute("SELECT animal_id from animaux_types"):
        a_types.append(row[0])
    if parent in a_types:
        types = {}
        for row in cursor.execute(f"SELECT type_id, pourcentage from animaux_types where animal_id={parent}"):
            types[int(row[0])] = float(row[1])
        return types
    for row in cursor.execute(f'SELECT velages.id, velages.mere_id, velages.pere_id, animaux_velages.animal_id, animaux_velages.velage_id from animaux_velages, velages where animaux_velages.animal_id="{parent}" and velages.id=animaux_velages.velage_id'):
        type1 = heritage_genetique(row[1]) # Mere
        type2 = heritage_genetique(row[2]) # Pere
        retl = {}
        for i in range(1,4):
            if not i in type1.keys():
                t1 = 0
            else:
                t1 = type1[i]
            if not i in type2.keys():
                t2 = 0
            else:
                t2 = type2[i]
            if not(t1 == 0 and t2 == 0):
                retl[i] = (t1 + t2)/2
        return retl

ids = []
for row in cursor.execute("SELECT id from animaux"):
    ids.append(row[0])

for i in ids:
    a_types = []
    for row in cursor.execute("SELECT animal_id, type_id from animaux_types"):
        a_types.append([row[0],row[1]])
    her = heritage_genetique(i)
    for j in her.items():
        if [i,j[0]] not in a_types:
            cursor.execute(f"INSERT INTO animaux_types (animal_id, type_id, pourcentage) VALUES ({int(i)},{int(j[0])},{float(j[1])});")
conn.commit()

conn.close()
