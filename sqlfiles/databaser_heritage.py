import sqlite3

# Connection à la base
conn = sqlite3.connect('Vaches.db')
cursor = conn.cursor()

def heritage_genetique(parent):
    """ Fonction recursive qui retourne le pourcentage de race de l'animal
    Pre : 'parent' est un id d'un animale et se trouve dans la base de données
    Post : Retourne un dictionnaire en format {'id de la race' : 'pourcentage'}
    """

    if parent in [i[0] for i in a_types]: # Si l'animal est présent dans la table animaux_types
        types = {int(row[0]) : float(row[1]) for row in cursor.execute(f"SELECT type_id, pourcentage from animaux_types where animal_id={parent}")} # Dictionnaire en format {'id du type' : 'pourcentage'}
        return types

    for row in cursor.execute(f'SELECT velages.id, velages.mere_id, velages.pere_id, animaux_velages.animal_id, animaux_velages.velage_id from animaux_velages, velages where animaux_velages.animal_id="{parent}" and velages.id=animaux_velages.velage_id'):
        type1 = heritage_genetique(row[1]) # Races de la Mere
        type2 = heritage_genetique(row[2]) # Races du Pere
        retl = {} # Dictionnaire en format {'id du type' : 'somme des pourcentage des parents'}
        for i in range(1,4): # On sait qu'il y a 3 types
            # Si l'animal possede 0% d'un type alors ce type ne sera pas dans le dictionnaire
            if not i in type1.keys():
                t1 = 0
            else:
                t1 = type1[i]
            if not i in type2.keys():
                t2 = 0
            else:
                t2 = type2[i]
            # Si un des deux parents ou les deux heritent de cette race alors enregistrer dans 'rectl'
            if not(t1 == 0 and t2 == 0):
                retl[i] = (t1 + t2)/2
        return retl

ids = [row[0] for row in cursor.execute("SELECT id from animaux")] # ID des animaux

a_types = [[row[0], row[1]] for row in cursor.execute("SELECT animal_id, type_id from animaux_types")] # Liste en format [['id de l'animal', 'id du type']]

for i in ids: # Pour chaque animal
    her = heritage_genetique(i) # Heritage genetique de l'animal
    for j in her.items(): # Pour chaque type et pourcentage
        if [i,j[0]] not in a_types: # Si id de l'animal et du type n'est pas présent dans la table animaux_types
            cursor.execute(f"INSERT INTO animaux_types (animal_id, type_id, pourcentage) VALUES ({int(i)},{int(j[0])},{float(j[1])});") # Inserer dans animaux_types les types et pourcentage de l'animal
            a_types.append([i,j[0]])
conn.commit() # Enregistrer

conn.close() # Terminer la connection
