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
    global Provincia_Trovato, Comuni_Trovati
    Provincia_Cercato = request.args['Provincia']
    Provincia_Trovato = Provincia[Provincia['DEN_UTS'] == Provincia_Cercato]
    Comuni_Trovati = Comune[Comune.within(Provincia_Trovato.unary_union)]
    area = Provincia_Trovato.geometry.area.sum()/ 10**6
    return render_template("Correzione_Verifica_2/area.html", area = area)

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))

    Comuni_Trovati.to_crs(epsg=3857).plot(ax=ax, edgecolor='r', facecolor = 'none')
    Provincia_Trovato.to_crs(epsg=3857).plot(ax=ax, edgecolor='k', facecolor = 'none')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)