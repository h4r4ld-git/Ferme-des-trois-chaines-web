
Lancement du site:

Pour lancer le site il suffit d'executer le fichier main.py avec python (version 3) sur un terminal (Linux), CMD ou powershell (pour windows)

Les packages nécessaires pour executer le programme sont flask et sqlite3
Pour installer ces packages:
$ pip install flask sqlite3

Pour Lancer le site:
$ python main.py

Ensuite le terminal ou cmd va afficher un lien url du site:
Exemple:
* Serving Flask app "main" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/

Fichiers et dossiers:

Vaches.db est la base de données qui contient tout les éléments nécessaires pour les figures et est généré dans le dossier sqlfiles à l'aide des programmes
database.py et database_heritage.py
Pour générer de nouveau ce fichier il suffit d'executer le fichier database.py en premier et ensuit database_heritage.py. L'ordre est trés important dans l'execution
Pour l'execution de database_heritage il faut patienter 1 ou 2 minutes mais il est possible de faire fonctionner le site sans ces éléments qui sont générés dans ce programme.

main.py contient le code qui permettra d'afficher les figures et lancer le site.

Le dossier sqlfiles contient tout les fichiers des requetes sql et les deux programmes qui générent la base de données Vaches.db

Le dossier static contient les fichiers CSS et JS qui permettent de décorer le site.

Le dossier templates contient les fichiers html.
