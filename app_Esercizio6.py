#realizzare un sito web chde resituisca la mappa dei quartieri di milano. 
#Ci deve essere un home page con un link'Quartiere di milano': Clicando su questo link si deve visualizzare la mappa su quartiere di milano
from flask import Flask, render_template, send_file, make_response, url_for, Response,request
app = Flask(__name__)

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



Quartiere = gpd.read_file('/workspace/Flask/ds964_nil_wm (1).zip')
Comuni = gpd.read_file('/workspace/Flask/Comuni.zip')
Fontanelle = gpd.read_file('/workspace/Flask/Fontanelle.zip')


@app.route('/', methods=['GET'])
def homePage():
    return render_template('app_Esercizio6/Form6.html')

@app.route('/quartieri', methods=['GET'])
def quartieri1():

    fig, ax = plt.subplots(figsize = (12,8))

    Quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot.png', methods=['GET'])
def plot_png():

    fig, ax = plt.subplots(figsize = (12,8))

    Quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/cerca', methods=['GET'])
def Cerca():

    fig, ax = plt.subplots(figsize = (12,8))
    Cerca = request.args('comune')
    Trovato = Comuni[Comuni['NIL'] == Cerca]

    Trovato.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/visualizza', methods=['GET'])
def Visualizza_dati():
    fig, ax = plt.subplots(figsize = (12,8))

    Quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/ricerca', methods=['GET'])
def ricerca():
    return render_template('app_Esercizio6/ricerca_Es6.html')

@app.route('/scelta', methods=['GET'])
def scelta():
    quartiere = Quartiere['NIL'].drop_duplicates().to_list()
    return render_template('app_Esercizio6/scelta_Es6.html',quartiere=quartiere)

@app.route('/fontanelle', methods=['GET'])
def fontanelle():
    quartiere = Quartiere['NIL'].drop_duplicates().to_list()
    quartiere.sort()
    return render_template('app_Esercizio6/fontanelle_Es6.html',quartiere=quartiere)


@app.route('/dati_ricerca', methods=['GET'])
def Ricerca_dati():
    Ricerca = request.args['ricerca']
    if Ricerca in list(Quartiere['NIL']):
        Trovato = Quartiere[Quartiere['NIL'] == Ricerca]
    
        fig, ax = plt.subplots(figsize = (12,8))

        Trovato.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
        contextily.add_basemap(ax=ax)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    else:
        return ('Quartiere non trovato.')

@app.route('/dati_scelta', methods=['GET'])
def Sceglie_dati():
    Scelta = request.args['Scelta']
    Trovato = Quartiere[Quartiere['NIL'] == Scelta]
    fig, ax = plt.subplots(figsize = (12,8))

    Trovato.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/dati_fontanelle', methods=['GET'])
def Fontanelle_dati():
    Scelta = request.args['Scelta']
    Trovato = Quartiere[Quartiere['NIL'] == Scelta]
    Fontanelle2 = Fontanelle[Fontanelle.within(Trovato.unary_union)]
    fig, ax = plt.subplots(figsize = (12,8))
    Trovato.to_crs(epsg=3857).plot(ax=ax,alpha=0.5,facecolor='g')

    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)