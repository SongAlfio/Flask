#realizzare un sito web chde resituisca la mappa dei quartieri di milano. 
#Ci deve essere un home page con un link'Quartiere di milano': Clicando su questo link si deve visualizzare la mappa su quartiere di milano
from flask import Flask, render_template, send_file, make_response, url_for, Response
app = Flask(__name__)

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



Quartiere = gpd.read_file('/workspace/Flask/ds964_nil_wm (1).zip').to_crs(epsg=3857)
Comuni = gpd.read_file('/workspace/Flask/Comuni.zip').to_crs(epsg=3857)


@app.route('/', methods=['GET'])
def homePage():
    return render_template('Form6_1.html')

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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)