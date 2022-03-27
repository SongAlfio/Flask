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




Regione = gpd.read_file("/workspace/Flask/Regioni.zip")
Province = gpd.read_file('/workspace/Flask/Provinci.zip')
Comune = gpd.read_file('/workspace/Flask/Comuni.zip')
Regione.to_html(header="true", table_id="table")
Province.to_html(header="true", table_id="table")
Comune.to_html(header="true", table_id="table")
@app.route('/', methods=['GET'])
def homePage():
    reg = Regione['DEN_REG'].drop_duplicates().to_list()
    return render_template("Form7.html",reg=reg)

@app.route('/dati', methods=['GET'])
def regione():
    Regione_Scelto = request.args['regione']
    Trovato = Regione[Regione['DEN_REG']==Regione_Scelto]
    Provincia = Province[Province.within(Trovato.unary_union)]
    return render_template("Provincia_Es7.html",Prov = Provincia['DEN_UTS'])

@app.route('/Comuni', methods=['GET'])
def comune():
    Provincia_Scelto = request.args['provincia']
    Trovato1 = Province[Province['DEN_UTS'] == Provincia_Scelto]
    Comune_Trovato = Comune[Comune.within(Trovato1.unary_union)]
    return render_template("Comune_Trovato_Es7.html",Comune_Trovato = Comune_Trovato['COMUNE'])

@app.route('/Plot', methods=['GET'])
def Plot():
        Comune_Scelto = request.args['{{Comune_Trovato}}']
        Plot = Comune[Comune['COMUNE']==Comune_Scelto]
        fig, ax = plt.subplots(figsize = (12,8))

        Plot.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
        contextily.add_basemap(ax=ax)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)