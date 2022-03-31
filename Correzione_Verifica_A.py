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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)