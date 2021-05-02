import sqlite3

# Connection à la base de données
conn = sqlite3.connect('Vaches.db')
cursor = conn.cursor()

# Executer le schéma de la base
cursor.execute('''CREATE TABLE IF NOT EXISTS "animaux" (
    "id" INT NOT NULL PRIMARY KEY,
    "famille_id" INT NOT NULL,
    "sexe" VARCHAR (255) NOT NULL,
    "presence" INT NOT NULL,
    "apprivoise" INT NOT NULL,
    "mort_ne" INT NOT NULL,
    "decede" INT NOT NULL,
    FOREIGN KEY ("famille_id") REFERENCES "familles" ("id"));''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "familles" (
    "id" INT NOT NULL PRIMARY KEY,
    "nom" VARCHAR (255) NOT NULL
  );''')

cursor.execute('''
  CREATE TABLE IF NOT EXISTS "types" (
    "id" INT NOT NULL PRIMARY KEY,
    "type" VARCHAR (255) NOT NULL
  );''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "animaux_types" (
    "animal_id" INT NOT NULL,
    "type_id" INT NOT NULL,
    "pourcentage" REAL NOT NULL,
    FOREIGN KEY ("animal_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("type_id") REFERENCES "types" ("id"),
    PRIMARY KEY ("animal_id", "type_id"),
    CHECK ("pourcentage" >= 0 AND "pourcentage" <= 100)
  );''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "velages" (
    "id" INT NOT NULL PRIMARY KEY,
    "mere_id" INT NOT NULL,
    "pere_id" INT NOT NULL,
    "date" DATE NOT NULL,
    FOREIGN KEY ("mere_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("pere_id") REFERENCES "animaux" ("id")
  );''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "animaux_velages" (
    "animal_id" INT NOT NULL,
    "velage_id" INT NOT NULL,
    FOREIGN KEY ("animal_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("velage_id") REFERENCES "velages" ("id"),
    PRIMARY KEY ("animal_id", "velage_id")
  );''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "complications" (
    "id" INT NOT NULL PRIMARY KEY,
    "complication" TEXT NOT NULL
  );''')
cursor.execute('''
  CREATE TABLE IF NOT EXISTS "velages_complications" (
    "velage_id" INT NOT NULL,
    "complication_id" INT NOT NULL,
    FOREIGN KEY ("velage_id") REFERENCES "velages" ("id"),
    FOREIGN KEY ("complication_id") REFERENCES "complications" ("id"),
    PRIMARY KEY ("velage_id", "complication_id")
   );''')

conn.commit() # Enregistrer

# Inserer les données dans la base
db_datas = ["insert_animaux.sql","insert_animaux_types.sql","insert_animaux_velages.sql","insert_complications.sql","insert_familles.sql","insert_types.sql","insert_velages.sql","insert_velages_complications.sql"]

for i in db_datas: # Executer chaque ligne dans chaque fichier de la liste db_datas
    with open(i, "r") as file:
        for j in file.read().split("\n"):
            cursor.execute(j)

conn.commit()

conn.close() # Terminer la connection
