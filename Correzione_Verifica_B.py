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


Stazioni = pd.read_csv('/workspace/Flask/templates/Correzione_Verifica_B/Radio.csv',sep=";")
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
Stazioni_Geo = gpd.read_file('/workspace/Flask/templates/Correzione_Verifica_B/Stazioni_Radio.geojson')
risultato = Stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index()

@app.route('/', methods=['GET'])
def homepage():
    return render_template("Correzione_Verifica_B/home.html")

@app.route('/radio', methods=['GET'])
def radio():
    Quartieri1 = Quartieri['NIL'].drop_duplicates().to_list()
    Quartieri1.sort()
    return render_template("Correzione_Verifica_B/Radio.html", quartieri = Quartieri1)

@app.route('/elenco', methods=['GET'])
def elenco():
    Quartiere = request.args['radio']
    Quartiere_Trovato = Quartieri[Quartieri['NIL'] == Quartiere]
    Stazioni_Radio = Stazioni_Geo[Stazioni_Geo.within(Quartiere_Trovato.unary_union)]

    return render_template('Correzione_Verifica_B/Elenco.html',Radio_Trovati = Stazioni_Radio['OPERATORE'].to_list())

@app.route('/input', methods=['GET'])
def input():
    return render_template("Correzione_Verifica_A/Input.html")

@app.route('/ricerca', methods=['GET'])
def ricerca():
    Quartiere_Cercato = request.args['ricerca']
    Quartiere_Trovato = Quartieri[Quartieri['NIL'].str.contains(Quartiere_Cercato)].to_crs(epsg=3857)
    Stazioni_Radio = Stazioni_Geo[Stazioni_Geo.to_crs(epsg=3857).within(Quartiere_Trovato.unary_union)]
    fig, ax = plt.subplots(figsize = (12,8))

    Stazioni_Radio.to_crs(epsg=3857).plot(ax=ax, facecolor='k', alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/numero', methods=['GET'])
def numero():
    return render_template("Correzione_Verifica_B/Elenco1.html",risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    fig, ax = plt.subplots(figsize = (6,4))

    x = risultato.MUNICIPIO
    y = risultato.OPERATORE

    ax.bar(x, y, color = "#304C89")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)