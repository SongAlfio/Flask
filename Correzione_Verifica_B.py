from flask import Flask, render_template, send_file, make_response, url_for, Response, request, redirect
app = Flask(__name__)
import pandas as pd
import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


Stazioni = pd.read_csv('/workspace/Flask/templates/Verifica_A/Radio.csv',sep=";")
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
Stazioni_Geo = gpd.read_file('/workspace/Flask/templates/Verifica_A/Stazioni_Radio.geojson')

@app.route('/', methods=['GET'])
def homepage():
    return render_template("Correzione_Verifica_B/home.html")

@app.route('/radio', methods=['GET'])
def radio():
    Quartieri1 = Quartieri['NIL'].drop_duplicates().to_list()
    Quartieri1.sort()
    return render_template("Correzione_Verifica_B/radio.html", quartieri = Quartieri1)

@app.route('/elenco', methods=['GET'])
def elenco():
    Quartiere = request.args['radio']
    Quartiere_Trovato = Quartieri[Quartieri['NIL']==Quartiere]
    Radio_Trovati = Quartiere_Trovato[Quartiere_Trovato.within(Stazioni_Geo.unary_union)].to_list()
    Radio_Trovati.sort()
    return render_template("Correzione_Verifica_B/elenco.html", Radio_Trovati = Radio_Trovati)