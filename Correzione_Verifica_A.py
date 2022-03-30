from flask import Flask, render_template, send_file, make_response, url_for, Response,request
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

# 1. Avere il numero di stazioni per ogni municipio (in ordine crescente sul numero del municipio) e il grafico corrispondente
Stazioni = pd.read_csv('/workspace/Flask/templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=";")
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
@app.route('/', methods=['GET'])
def homepage():
    return render_template("home.html")

@app.route('/numero', methods=['GET'])
def numero():
#numero stazioni per ogni municipio
    risultato = Stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index()
    return render_template("Elenco.html",risultato = risultato.to_html())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)