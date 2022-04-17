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


Bus_Tram = gpd.read_file('/workspace/Flask/Bus_Tram.zip')
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')


@app.route('/', methods=['GET'])
def homepage():
    return render_template("Correzione_Verifica_C/home.html")

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args['scelta']
    if scelta == 'Esercizio1':
        return redirect(url_for('input'))
    elif scelta == 'Esercizio2':
        return redirect(url_for('input1'))
    else:
        return redirect(url_for('scelta'))


@app.route('/input', methods=['GET'])
def input():
    return render_template("Correzione_Verifica_C/Input.html")

@app.route('/elenco', methods=['GET'])
def elenco():
    L_Minima = request.args['elenco1']
    L_Massima = request.args['elenco2']
    Bus_Tram1 = Bus_Tram[(Bus_Tram['lung_km'] < L_Massima) & (Bus_Tram['lung_km'] > L_Minima)]
    Bus_Tram1 = Bus_Tram1['linea'].drop_duplicates().to_list()
    Bus_Tram1.sort(key=int)
    return render_template("Correzione_Verifica_C/Elenco.html",Bus_Tram = Bus_Tram1)

@app.route('/input1', methods=['GET'])
def input1():
    return render_template("Correzione_Verifica_C/Input1.html")

@app.route('/elenco1', methods=['GET'])
def elenco1():
    Quartiere_Cercato = request.args['quartiere']
    Quartiere_Trovato = Quartieri[Quartieri['NIL'].str.contains(Quartiere_Cercato)]
    Bus_Tram1 = Bus_Tram[Bus_Tram.intersects(Quartiere_Trovato.unary_union)]
    Bus_Tram1 = Bus_Tram1['linea'].drop_duplicates().to_list()
    Bus_Tram1.sort(key=int)
    return render_template("Correzione_Verifica_C/Elenco.html",Bus_Tram = Bus_Tram1)

@app.route('/scelta', methods=['GET'])
def scelta():
    Bus_Tram1 = Bus_Tram['linea'].drop_duplicates().to_list()
    Bus_Tram1.sort(key=int)
    return render_template("Correzione_Verifica_C/Scelta.html",linea = Bus_Tram1)

@app.route('/linea', methods=['GET'])
def Plot():
        Linea_Scelto = request.args['linee']
        Plot = Bus_Tram[Bus_Tram['linea']==Linea_Scelto]
        fig, ax = plt.subplots(figsize = (12,8))

        Plot.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
        contextily.add_basemap(ax=ax)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)