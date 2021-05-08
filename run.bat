py -m venv venv
CALL venv\Scripts\activate
set FLASK_APP=flaskr
set FLASK_ENV=development
flask init-db
flask run
