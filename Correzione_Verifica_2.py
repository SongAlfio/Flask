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

Regione = gpd.read_file("/workspace/Flask/Regioni.zip")
Provincia = gpd.read_file('/workspace/Flask/Provinci.zip')
Comune = gpd.read_file('/workspace/Flask/Comuni.zip')
Ripartizione = gpd.read_file('/workspace/Flask/Italia.zip')

@app.route('/', methods=['GET'])
def home():
    return render_template("Correzione_Verifica_2/home.html")

@app.route('/link1', methods=['GET'])
def link1():
    return render_template("Correzione_Verifica_2/link1.html")

@app.route('/area', methods=['GET'])
def area():
    global Provincia_Trovata, Comuni_Trovati
    Provincia_Cercato = request.args['Provincia']
    Provincia_Trovata = Provincia[Provincia['DEN_UTS'] == Provincia_Cercato]
    Comuni_Trovati = Comune[Comune.within(Provincia_Trovata.unary_union)]
    area = Provincia_Trovata.geometry.area.sum()/ 10**6
    return render_template("Correzione_Verifica_2/area.html", area = area)

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    Comuni_Trovati.to_crs(epsg=3857).plot(ax=ax, edgecolor='r', facecolor = 'none')
    Provincia_Trovata.to_crs(epsg=3857).plot(ax=ax, edgecolor='k', facecolor = 'none')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/link2', methods=['GET'])
def link2():
    REG = Regione['DEN_REG'].drop_duplicates().to_list()
    REG.sort()
    return render_template("Correzione_Verifica_2/link2.html", REG = REG)

@app.route('/link2_1', methods=['GET'])
def link2_1():
    Regione_Scelto = request.args['Regione']
    Regione_Trovato = Regione[Regione['DEN_REG']==Regione_Scelto]
    Provinci_Trovati = Provincia[Provincia.within(Regione_Trovato.unary_union)]
    Provinci_Trovati = Provinci_Trovati['DEN_UTS'].drop_duplicates().to_list()
    Provinci_Trovati.sort()
    return render_template("Correzione_Verifica_2/link2_1.html", Prov = Provinci_Trovati)

@app.route('/area1', methods=['GET'])
def area1():
    global Provincia_Trovata1, Comuni_Trovati1
    Provincia_Scelta = request.args['Provincia']
    Provincia_Trovata1 = Provincia[Provincia['DEN_UTS'] == Provincia_Scelta]
    Comuni_Trovati1 = Comune[Comune.within(Provincia_Trovata1.unary_union)]
    area = Provincia_Trovata1.geometry.area.sum()/ 10**6
    return render_template("Correzione_Verifica_2/area1.html", area = area)

@app.route('/mappa1', methods=['GET'])
def mappa1():
    fig, ax = plt.subplots(figsize = (12,8))

    Comuni_Trovati1.to_crs(epsg=3857).plot(ax=ax, edgecolor='r', facecolor = 'none')
    Provincia_Trovata1.to_crs(epsg=3857).plot(ax=ax, edgecolor='k', facecolor = 'none')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/link3', methods=['GET'])
def link3():
    Rip = Ripartizione['DEN_REG'].drop_duplicates().to_list()
    Rip.sort()
    return render_template("Correzione_Verifica_2/link3.html", Rip=Rip)

@app.route('/link3_1', methods=['GET'])
def link3_1():
    Ripartizione_Scelto = request.args['Ripartizione']
    Ripartizione_Trovato = Ripartizione[Ripartizione['DEN_REG']==Ripartizione_Scelto]
    Provinci_Trovati = Provincia[Provincia.within(Regione_Trovato.unary_union)]
    Provinci_Trovati = Provinci_Trovati['DEN_UTS'].drop_duplicates().to_list()
    Provinci_Trovati.sort()
    return render_template("Correzione_Verifica_2/link3_1.html", Prov = Provinci_Trovati)

@app.route('/area2', methods=['GET'])
def area2():
    global Provincia_Trovata2, Comuni_Trovati2
    Provincia_Scelta = request.args['Provincia']
    Provincia_Trovata1 = Provincia[Provincia['DEN_UTS'] == Provincia_Scelta]
    Comuni_Trovati1 = Comune[Comune.within(Provincia_Trovata1.unary_union)]
    area = Provincia_Trovata1.geometry.area.sum()/ 10**6
    return render_template("Correzione_Verifica_2/area2.html", area = area)

@app.route('/mappa2', methods=['GET'])
def mappa2():
    fig, ax = plt.subplots(figsize = (12,8))

    Comuni_Trovati2.to_crs(epsg=3857).plot(ax=ax, edgecolor='r', facecolor = 'none')
    Provincia_Trovata2.to_crs(epsg=3857).plot(ax=ax, edgecolor='k', facecolor = 'none')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)