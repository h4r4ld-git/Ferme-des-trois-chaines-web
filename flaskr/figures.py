from flask import Blueprint, render_template, request, redirect, url_for
from flaskr.db import get_db
import datetime, calendar

bp = Blueprint('figures', __name__)

@bp.route('/')
def index():
    return redirect(url_for('figures.figure1'))

@bp.route('/home')
def home():
    return render_template('figures/home.html')

@bp.route('/figure1')
def figure1():
    data = figure1Data()
    return render_template('figures/figure1.html', dateSelected = data['dateSelected'], dates = data['dates'], nextMonth = data['nextMonth'], previousMonth = data['previousMonth'])

@bp.route('/figure2')
def figure2():
    return render_template('figures/figure2.html', query_result = figure2Data())

@bp.route('/figure3')
def figure3():
    return render_template('figures/figure3.html', query_result = figure3Data())

def figure1Data(year = None, month = None):

    if year == None:
        year = request.args.get('year')
    if month == None:
        month = request.args.get('month')

    now = datetime.datetime.now()

    if year == None:
        year = 2020
    else:
        if year.isdigit() or (year[0] == "-" and year[1:].isdigit()):
            year = int(year)
            if year > now.year:
                year = now.year
            if year < datetime.MINYEAR:
                year = datetime.MINYEAR
        else:
            year = now.year

    if month == None:
        if year == now.year:
            month = now.month
        else:
            month = 1
    else:
        if month.isdigit() or (month[0] == "-" and month[1:].isdigit()):
            month = int(month)
            if month > 12:
                month = 12
            if month < 1:
                month = 1
        else:
            month = 1

    dateSelected = datetime.datetime(year, month, 1)

    query = (
    'SELECT DATE(SUBSTR(V.date, 7, 4) || \'-\' || SUBSTR(V.date, 4, 2) || \'-\' || SUBSTR(V.date, 1, 2)) AS date, COUNT(V.date) AS nombre_de_naissance '
    'FROM velages V '
    'WHERE DATE(SUBSTR(V.date, 7, 4) || \'-\' || SUBSTR(V.date, 4, 2) || \'-\' || SUBSTR(V.date, 1, 2)) >= DATE(:date, \'start of month\') '
    'AND DATE(SUBSTR(V.date, 7, 4) || \'-\' || SUBSTR(V.date, 4, 2) || \'-\' || SUBSTR(V.date, 1, 2)) <= DATE(:date, \'start of month\', \'+1 month\', \'-1 day\') '
    'GROUP BY V.date '
    'ORDER BY V.date ASC'
    )

    velageDates = get_db().execute(query, {"date": dateSelected}).fetchall()

    dates = {}

    numberDayInMonth = calendar.monthrange(dateSelected.year, dateSelected.month)[1]

    for day in range(1, numberDayInMonth):
        dates[datetime.datetime(dateSelected.year, dateSelected.month, day)] = 0

    for velageDate in velageDates:
        dates[datetime.datetime(
            int(velageDate['date'][0:4]), 
            int(velageDate['date'][5:7]),
            int(velageDate['date'][8:10])
        )] = velageDate['nombre_de_naissance']

    nextMonth = dateSelected + datetime.timedelta(days = 45)
    previousMonth = dateSelected - datetime.timedelta(days = 15)

    return {'dateSelected': dateSelected, 'dates': dates, 'nextMonth': nextMonth, 'previousMonth': previousMonth}

def figure2Data():

    query = (
    'SELECT SUBSTR(V.date,4,2), CAST(COUNT(*) AS float)/30.0 '
    'FROM animaux A, velages V, animaux_velages AV '
    'WHERE A.mort_ne = 1 AND AV.animal_id = A.id AND AV.velage_id = V.id '
    'GROUP BY SUBSTR(V.date, 4, 2)'
    )

    # [Nombres de mort_nés de 1991 et 2020 dans l'ordre selon les mois, divisé par 30]
    return get_db().execute(query).fetchall() # [(mois, nombre de mort_nés)]

def figure3Data():

    query = (
    'SELECT nom, (SELECT CAST(COUNT(*) AS float) '
    'FROM animaux A '
    'WHERE A.famille_id=familles.id AND A.decede=1)/( '
        'SELECT CAST(COUNT(*) AS float) '
        'FROM animaux A '
        'WHERE A.famille_id=familles.id AND A.decede=0)*100 '
    'FROM animaux A '
    'LEFT JOIN familles '
    'ON A.famille_id=familles.id '
    'GROUP BY nom '
    )

    # [noms des familles, les proportions]
    return get_db().execute(query).fetchall()
