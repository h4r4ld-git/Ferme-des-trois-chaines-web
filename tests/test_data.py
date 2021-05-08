import sqlite3
import pytest
from flaskr.db import get_type_quantite, init_db
from flaskr.figures import figure1_data, figure2_data, figure3_data
from flaskr import create_app


app = create_app()

def test_heritage():
    with app.app_context():
        init_db()
        assert get_type_quantite() == [('Blanc Bleu Belge', 144), ('Holstein', 4276), ('Jersey', 49)] , "Test sur le nombre d'animal de chaque type"

def test_f1():
    with app.app_context():
        data = figure1_data()
        assert data[1][26] == 3.9 , "Test pour le nombre de naissance du 27"
        assert data[1][1] == 4.3 , "Test pour le nombre de naissance du 2"
        assert data[1][2] == 4.5 , "Test pour le nombre de naissance du 3"

def test_f2():
    with app.app_context():
        data = figure2_data()
        assert data[6] == 0.5 , "Test pour le nombre de mort-né en juillet"
        assert data[2] == 0.7 , "Test pour le nombre de mort-né en mars"
        assert data[5] == 0.6 , "Test pour le nombre de mort-né en juin"

def test_f3():
    with app.app_context():
        f3_data = figure3_data()
        data = {f3_data[0][i]: f3_data[1][i] for i in range(len(f3_data[0]))}
        assert data["Kinder"] == 100.0 , "Test pour la famille Kinder"
        assert data["Mercedes"] == 100.0 , "Test pour la famille Mercedes"
        assert data["Madi"] == pytest.approx(14.2857142857142) , "Test pour la famille Madi"
