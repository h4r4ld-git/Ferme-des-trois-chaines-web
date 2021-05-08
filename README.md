# LINFO1002_2021_P2_1A_6
## Execution pour Linux ou MacOS

```
$ sh run.sh
```


## Execution pour Windows

Pour lancer le site sur windows il suffit d'executer le fichier run.bat.

## Outils

Pour faire fonctionner le site vous avez besoin de python (version 3) et ses modules flask et sqlite3.
Pour installer les modules flask et sqlite3 il faut executer les commandes suivantes
```
$ pip3 install flask sqlite3
```
Vous avez aussi besoin le package virtualenv de python.
Pour l'installer il faut executer la commande suivante
```
$ pip3 install virtualenv
```
## Arborescence
```
.
├── captures_d_ecran
│   ├── capt1.png
│   └── capt2.png
├── flaskr
│   ├── data
│   │   ├── insert_animaux.sql
│   │   ├── insert_animaux_types.sql
│   │   ├── insert_animaux_velages.sql
│   │   ├── insert_complications.sql
│   │   ├── insert_familles.sql
│   │   ├── insert_types.sql
│   │   ├── insert_velages_complications.sql
│   │   ├── insert_velages.sql
│   │   └── schema.sql
│   ├── db.py
│   ├── figures.py
│   ├── __init__.py
│   ├── README.md
│   ├── static
│   │   ├── bg.jpg
│   │   ├── bg.png
│   │   ├── bootstrap.css
│   │   ├── chart.min.js
│   │   └── favicon.png
│   └── templates
│       └── base.html
├── instance
│   ├── flaskr.sqlite
│   └── test.py
├── run.bat
└── run.sh

```
Les requetes SQL sont executer par le fichier flaskr/db.py avec la commande `flask init-db`.
Le fichier flaskr/figures.py permet de recuperer les données nécessaires de la base de données et afficher les graphes sur le site.
Les repertoires static et templates dans flaskr contiennent les styles (CSS, JS, bootstrap, images) et le code html du site.
Le repertoire data dans flaskr contient les fichiers sql avec toutes le requetes SQL.

## Images

![alt text](captures_d_ecran/capt1.png)
![alt text](captures_d_ecran/capt2.png)
