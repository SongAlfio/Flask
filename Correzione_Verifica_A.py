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

# 1. Avere il numero di stazioni per ogni municipio (in ordine crescente sul numero del municipio) e il grafico corrispondente
Stazioni = pd.read_csv('/workspace/Flask/templates/Verifica_A/Radio.csv',sep=";")
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
Stazioni_Geo = gpd.read_file('/workspace/Flask/templates/Verifica_A/Stazioni_Radio.geojson')
risultato = Stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index()
@app.route('/', methods=['GET'])
def homepage():
    return render_template("Verifica_A/home1.html")

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args['scelta']
    if scelta == 'Esercizio1':
        return redirect(url_for('numero'))#重新定向
    elif scelta == 'Esercizio2':
        return redirect(url_for('input'))
    else:
        return redirect(url_for('dropdown'))
@app.route('/numero', methods=['GET'])
def numero():
#numero stazioni per ogni municipio
    
    return render_template("Verifica_A/Elenco.html",risultato = risultato.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
#Costruzione del grafico
    fig, ax = plt.subplots(figsize = (6,4))

    x = risultato.MUNICIPIO
    y = risultato.OPERATORE

    ax.bar(x, y, color = "#304C89")
#visualizzazione del grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/input', methods=['GET'])
def input():
#input quartiere
    
    return render_template("Verifica_A/Input.html")

@app.route('/ricerca', methods=['GET'])
def ricerca():
#cercare il quartiere
    Quartiere_Cercato = request.args['ricerca']
    Quartiere_Trovato = Quartieri[Quartieri['NIL'].str.contains(Quartiere_Cercato)]
    Stazioni_Radio = Stazioni_Geo[Stazioni_Geo.within(Quartiere_Trovato.unary_union)]
    #fig, ax = plt.subplots(figsize = (12,8))

    #Stazioni_Radio.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    #contextily.add_basemap(ax=ax)
    #output = io.BytesIO()
    #FigureCanvas(fig).print_png(output)
    #return Response(output.getvalue(), mimetype='image/png')
    return render_template('Verifica_A/Elenco1.html',risultato = Stazioni_Radio.to_html())
    
@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    Stazioni_Radio.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    Quartiere_Cercato.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/dropdown', methods=['GET'])
def dropdown():
    Nomi_Stazioni = Stazioni['OPERATORE'].drop_duplicates().to_list()
    #oppure possiamo fare Nomi_Stazioni = list(set(Nomi_Stazioni))
    Nomi_Stazioni.sort()
    
    return render_template('Verifica_A/Dropdown.html',stazioni = Nomi_Stazioni)

@app.route('/scelta_stazione', methods=['GET'])
def scelta():
    global Stazione_Utente, quartiere
    Stazione_Scelta = request.args['stazione']
    Stazione_Utente = Stazioni_Geo[Stazioni_Geo.OPERATORE==Stazione_Scelta]
    quartiere = Quartieri[Quartieri.contains(Stazione_Utente.geometry.squeeze())]
    return render_template('Verifica_A/Lista_Stazione.html',quartiere = quartiere['NIL'])

@app.route('/mappa_quartiere', methods=['GET'])
def mappa_quartiere():
    fig, ax = plt.subplots(figsize = (12,8))

    Stazioni_Utente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)