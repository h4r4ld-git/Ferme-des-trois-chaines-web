import sqlite3, pytest, datetime
from flaskr.db import get_type_quantite
from flaskr.figures import figure1Data, figure2Data, figure3Data
from flaskr import create_app

app = create_app()

def test_heritage():
    with app.app_context():
        assert get_type_quantite() == [('Blanc Bleu Belge', 144), ('Holstein', 4276), ('Jersey', 49)] , "Test sur le nombre d'animal de chaque type"

def test_f1():
    with app.app_context():
        data = figure1Data(year = "2019", month = "12")
        assert data["dates"][datetime.datetime(2019, 12, 1)] == 1 , "Test pour le nombre de naissance du 1/12/2019"
        assert data["dates"][datetime.datetime(2019, 12, 2)] == 3 , "Test pour le nombre de naissance du 2/12/2019"
        assert data["dates"][datetime.datetime(2019, 12, 3)] == 0 , "Test pour le nombre de naissance du 3/12/2019"
        assert data["dates"][datetime.datetime(2019, 12, 18)] == 0 , "Test pour le nombre de naissance du 18/12/2019"
        assert data["dates"][datetime.datetime(2019, 12, 19)] == 3 , "Test pour le nombre de naissance du 19/12/2019"
        assert data["dates"][datetime.datetime(2019, 12, 20)] == 0 , "Test pour le nombre de naissance du 20/12/2019"

def test_f2():
    with app.app_context():
        data = figure2Data()
        assert data[6][1] == 0.5 , "Test pour le nombre de mort-né en juillet"
        assert data[2][1] == 0.7 , "Test pour le nombre de mort-né en mars"
        assert data[5][1] == 0.6 , "Test pour le nombre de mort-né en juin"

def test_f3():
    with app.app_context():
        f3_data = figure3Data()
        data = {f3_data[i][0]: f3_data[i][1] for i in range(len(f3_data))}
        assert data["Kinder"] == 100.0 , "Test pour la famille Kinder"
        assert data["Mercedes"] == 100.0 , "Test pour la famille Mercedes"
        assert data["Madi"] == pytest.approx(14.2857142857142) , "Test pour la famille Madi"
