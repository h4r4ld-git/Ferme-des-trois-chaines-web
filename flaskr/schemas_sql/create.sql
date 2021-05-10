BEGIN TRANSACTION;

  DROP TABLE IF EXISTS "animaux";
  DROP TABLE IF EXISTS "familles";
  DROP TABLE IF EXISTS "types";
  DROP TABLE IF EXISTS "animaux_types";
  DROP TABLE IF EXISTS "velages";
  DROP TABLE IF EXISTS "animaux_velages";
  DROP TABLE IF EXISTS "complications";
  DROP TABLE IF EXISTS "velages_complications";

  CREATE TABLE "animaux" (
    "id" INT NOT NULL PRIMARY KEY,
    "famille_id" INT NOT NULL,
    "sexe" TEXT NOT NULL,
    "presence" INT NOT NULL,
    "apprivoise" INT NOT NULL,
    "mort_ne" INT NOT NULL DEFAULT 0,
    "decede" INT NOT NULL DEFAULT 0,
    FOREIGN KEY ("famille_id") REFERENCES "familles" ("id")
  );
  
  CREATE TABLE "familles" (
    "id" INT NOT NULL PRIMARY KEY,
    "nom" TEXT NOT NULL
  );

  CREATE TABLE "types" (
    "id" INT NOT NULL PRIMARY KEY,
    "type" TEXT NOT NULL
  );

  CREATE TABLE "animaux_types" (
    "animal_id" INT NOT NULL,
    "type_id" INT NOT NULL,
    "pourcentage" REAL NOT NULL,
    FOREIGN KEY ("animal_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("type_id") REFERENCES "types" ("id"),
    PRIMARY KEY ("animal_id", "type_id"),
    CHECK ("pourcentage" >= 0 AND "pourcentage" <= 100)
  );

  CREATE TABLE "velages" (
    "id" INT NOT NULL PRIMARY KEY,
    "mere_id" INT NOT NULL,
    "pere_id" INT NOT NULL,
    "date" DATE NOT NULL,
    FOREIGN KEY ("mere_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("pere_id") REFERENCES "animaux" ("id")
  );

  CREATE TABLE "animaux_velages" (
    "animal_id" INT NOT NULL,
    "velage_id" INT NOT NULL,
    FOREIGN KEY ("animal_id") REFERENCES "animaux" ("id"),
    FOREIGN KEY ("velage_id") REFERENCES "velages" ("id"),
    PRIMARY KEY ("animal_id", "velage_id")
  );

  CREATE TABLE "complications" (
    "id" INT NOT NULL PRIMARY KEY,
    "complication" TEXT NOT NULL
  );

  CREATE TABLE "velages_complications" (
    "velage_id" INT NOT NULL,
    "complication_id" INT NOT NULL,
    FOREIGN KEY ("velage_id") REFERENCES "velages" ("id"),
    FOREIGN KEY ("complication_id") REFERENCES "complications" ("id"),
    PRIMARY KEY ("velage_id", "complication_id")
  );

COMMIT;