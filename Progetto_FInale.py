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


Occupazione = gpd.read_file('https://dati.comune.milano.it/dataset/6efe2c8c-e1f6-4411-a061-df1e0d7a69ab/resource/6538b1ca-3545-4eb4-9e11-12136650aa35/download/geopost_layer_0_m_public_info_owner_street_statuspoint_4326_final.geojson')
Ristoranti = gpd.read_file('https://dati.comune.milano.it/dataset/f0671ce0-8c11-4ee8-95e5-c09913d00f83/resource/1623c617-028c-4f8a-9919-7f314701f50a/download/economia_pubblici_esercizi_in_piano.geojson')
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
Ristoranti = Ristoranti.dropna(subset=['denominazione_pe','LONG_WGS84','LAT_WGS84'])

@app.route('/', methods=['GET'])
def homepage():
    return render_template("Progetto_Finale/home.html")

# Visualizzazione di milano e le occupazioni
@app.route('/mappa_milano', methods=['GET'])
def mappa_milano():
    fig, ax = plt.subplots(figsize = (12,8))

    Quartieri.to_crs(epsg=3857).plot(ax=ax, facecolor='none', edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Inserimento quartiere e visualizazzione mappa delle Ristoranti
@app.route('/Cerca_Quartiere', methods=['GET'])
def Cerca():
    return render_template("Progetto_Finale/Cerca_Quartiere.html")

@app.route('/Mappa_Quartiere_Ristoranti', methods=['GET'])
def Mappa_Quartiere_Ristoranti():
    Quartiere = request.args('Quartiere')
    Quartiere_Trovato = Quartieri[Quartieri['NIL'] == 'Quartiere']
    Quartiere_Ristorante = Ristoranti[Ristoranti.within(Quartiere_Trovato.unary_union)]

    fig, ax = plt.subplots(figsize = (12,8))

    Quartieri.to_crs(epsg=3857).plot(ax=ax, facecolor='none', edgecolor = 'k')
    Risto.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Numero di  Ristoranti per ogni quartiere (grafico a barre)
@app.route('/Numeri_Ristoranti', methods=['GET'])
def Numeri_Ristoranti():
    global Quartieri_Ristoranti1
    Quartieri1 = Quartieri.to_crs(epsg=3857)
    Ristoranti1 = Ristoranti.to_crs(epsg=3857)
    Quartieri_Ristoranti = gpd.sjoin(Ristoranti1,Quartieri1,how='left',op='intersects')
    Quartieri_Ristoranti1 = Quartieri_Ristoranti.groupby('NIL_right').count()[['Codice']].reset_index()
    return render_template("Progetto_Finale/Grafico.html", Quartieri_Ristoranti1 = Quartieri_Ristoranti1.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    fig, ax = plt.subplots(figsize = (20,10))

    x = Quartieri_Ristoranti1.NIL_right
    y = Quartieri_Ristoranti1.Codice

    ax.bar(x, y, color = "#304C89")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# l'utente inserisce un municipio e trova gli occupazioni di  quel municipio
@app.route('/Cerca_Municipio', methods=['GET'])
def Cerca_Municipio():
    return render_template("Progetto_Finale/Cerca_Municipio.html")

@app.route('/Mappa_Municipio_Ristoranti', methods=['GET'])
def Mappa_Municipio_Ristoranti():
    Municipio = request.args('Municipio')
    Municipio_Trovato = Municipio[Municipio[''] == 'Quartiere']
    Quartiere_Ristorante = Ristoranti[Ristoranti.within(Quartiere_Trovato.unary_union)]

    fig, ax = plt.subplots(figsize = (12,8))

    Quartieri.to_crs(epsg=3857).plot(ax=ax, facecolor='none', edgecolor = 'k')
    Risto.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)