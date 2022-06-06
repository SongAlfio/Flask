from flask import Flask, render_template, send_file, make_response, url_for, Response, request, redirect
app = Flask(__name__)
import pandas as pd
import io
import geopandas as gpd
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import folium

Occupazione = gpd.read_file('https://dati.comune.milano.it/dataset/6efe2c8c-e1f6-4411-a061-df1e0d7a69ab/resource/6538b1ca-3545-4eb4-9e11-12136650aa35/download/geopost_layer_0_m_public_info_owner_street_statuspoint_4326_final.geojson')
Ristoranti = gpd.read_file('https://dati.comune.milano.it/dataset/f0671ce0-8c11-4ee8-95e5-c09913d00f83/resource/1623c617-028c-4f8a-9919-7f314701f50a/download/economia_pubblici_esercizi_in_piano.geojson')
Quartieri = gpd.read_file('/workspace/Flask/Quartieri.zip')
Municipi = gpd.read_file('/workspace/Flask/Municipio.geojson')
Ristoranti = Ristoranti.dropna(subset=['denominazione_pe','LONG_WGS84','LAT_WGS84'])
Quartieri['NIL'] = Quartieri['NIL'].str.lower()
Ristoranti['denominazione_pe'] = Ristoranti['denominazione_pe'].str.lower()

@app.route('/', methods=['GET'])
def homepage():
    return render_template("Progetto_Finale/sito1nice.html")

@app.route('/Home', methods=['GET'])
def home():
    return render_template("Progetto_Finale/link_Pr.html")
    
# Visualizzazione di milano
@app.route('/Mappa', methods=['GET'])
def Mappa():
    return render_template("Progetto_Finale/Mappa.html")

@app.route('/mappa_milano', methods=['GET'])
def mappa_milano():
    fig, ax = plt.subplots(figsize = (12,8))
    Quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, facecolor='k')
    ctx.add_basemap(ax=ax)
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
    Quartieri_Ristoranti1 = Quartieri_Ristoranti.groupby('NIL_right').count()[['insegna']].reset_index()
    return render_template("Progetto_Finale/Grafico.html", Quartieri_Ristoranti1 = Quartieri_Ristoranti1.to_html())

@app.route('/grafico', methods=['GET'])
def grafico():
    fig, ax = plt.subplots(figsize = (10,15))

    x = Quartieri_Ristoranti1.NIL_right
    y = Quartieri_Ristoranti1.insegna


    ax.barh(x, y, color = "#304C89")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Inserimento quartiere e visualizazzione mappa delle Ristoranti
@app.route('/Cerca_Quartiere', methods=['GET'])
def Cerca():
    Quartieri1 = Quartieri.drop_duplicates().sort_values('NIL').reset_index()
    return render_template("Progetto_Finale/Cerca_Quartiere.html", Quartieri = Quartieri1[['NIL']].to_html())

@app.route('/Mappa_Quartiere_Ristoranti', methods=['GET'])
def Mappa_Quartiere_Ristoranti():
    Quartiere = request.args['Quartiere'].lower()
    if Quartiere in list(Quartieri['NIL']):
        Quartiere_Trovato = Quartieri[Quartieri['NIL'] == Quartiere]
        Quartiere_Ristorante = Ristoranti[Ristoranti.within(Quartiere_Trovato.unary_union)]
        
        m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
        for _, r in Quartiere_Trovato.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.0001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
            folium.Popup(r['NIL']).add_to(geo_j)
            geo_j.add_to(m)
        for _, row in Quartiere_Ristorante.dropna().iterrows():
          folium.Marker(
              location=[row["LAT_WGS84"], row["LONG_WGS84"]],
              popup=row['denominazione_pe'],
              icon=folium.map.Icon(color='lightblue')
              ).add_to(m)
        return m._repr_html_()
    else:
        return render_template("Progetto_Finale/Errore.html",Errore = Quartiere)

# l'utente inserisce un municipio e trova gli occupazioni di  quel municipio
@app.route('/Cerca_Municipio', methods=['GET'])
def Cerca_Municipio():
    return render_template("Progetto_Finale/Cerca_Municipio.html")

@app.route('/Mappa_Municipio_Ristoranti', methods=['GET'])
def Mappa_Municipio_Ristoranti():
    Municipio = request.args['Municipio']
    Municipio = int(Municipio)
    if Municipio in list(Ristoranti['MUNICIPIO'].dropna().astype('int64')):
        Ristoranti['MUNICIPIO'] = Ristoranti['MUNICIPIO'].dropna().astype('int64')
        Ristoranti_Trovati = Ristoranti[Ristoranti['MUNICIPIO'] == Municipio]
        Municipio_Trovato = Municipi[Municipi['MUNICIPIO'] == Municipio]
        m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
        for _, r in Municipio_Trovato.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.0001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
            folium.Popup(r['MUNICIPIO']).add_to(geo_j)
            geo_j.add_to(m)
        for _, row in Ristoranti_Trovati.iterrows():
            folium.Marker(
                location=[row["LAT_WGS84"], row["LONG_WGS84"]],
                popup=row['denominazione_pe'],
                icon=folium.map.Icon(color='lightblue')
            ).add_to(m)
        
        return m._repr_html_()
    else:
        return render_template("Progetto_Finale/Errore.html",Errore = Municipio)

# l'utente inserisce un tipo di posto che vuole andare(bar; ristorante...) o il nome del ristorante
@app.route('/Cerca_Posto', methods=['GET'])
def Cerca_Posto():
    return render_template("Progetto_Finale/Cerca_Posto.html")

@app.route('/Mappa_Posto', methods=['GET'])
def Mappa_Posto():
    Posto = request.args['Posto'].lower()
    Ristoranti2=Ristoranti['denominazione_pe'].str.lower().dropna().to_list()
    Ristoranti1 = Ristoranti.dropna()
    Ristoranti3=Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Posto)]['denominazione_pe'].to_list()
    if len(Ristoranti3) != 0:
            Ristorante_Trovato = Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Posto)]
            m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
            for _, row in Ristorante_Trovato.iterrows():
                folium.Marker( 
                    location=[row["LAT_WGS84"], row["LONG_WGS84"]],
                    popup=row['denominazione_pe'],
                    icon=folium.map.Icon(color='lightblue')
                ).add_to(m)
            return m._repr_html_()
    else:
            return render_template("Progetto_Finale/Errore.html",Errore = Posto)


# l'utente inserisce il nome che vuole cercare e anche il posto che sta, trova tutti i ristoranti in quel posto
@app.route('/Cerca_Ristoranti', methods=['GET'])
def Cerca_Ristoranti():
    return render_template("Progetto_Finale/Cerca_Ristoranti.html")

@app.route('/scelta', methods=['GET'])
def scelta():
    Risposta = request.args['scelta']
    if Risposta == 'Quartiere':
        Quartieri1 = Quartieri.drop_duplicates().sort_values('NIL').reset_index()
        return render_template("Progetto_Finale/Cerca_Ristoranti_Quartiere.html",Quartieri = Quartieri1[['NIL']].to_html())
    if Risposta == 'Municipio':
        return render_template("Progetto_Finale/Cerca_Ristoranti_Municipio.html")

@app.route('/Mappa_Ristoranti_Quartiere', methods=['GET'])
def Mappa_Ristoranti_Quartiere():
    Ristorante = request.args['Ristorante'].lower()
    Quartiere = request.args['Quartiere'].lower()
    Ristoranti2=Ristoranti['denominazione_pe'].str.lower().dropna().to_list()
    Ristoranti1 = Ristoranti.dropna()
    Ristoranti3=Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Ristorante)]['denominazione_pe'].to_list()
    if len(Ristoranti3) != 0:
        if Quartiere in list(Quartieri['NIL']):
            Ristorante_Trovato = Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Ristorante)]
            Quartiere_Trovato = Quartieri[Quartieri['NIL']==Quartiere]
            Ristoranti_Quartiere = Ristorante_Trovato[Ristorante_Trovato.within(Quartiere_Trovato.unary_union)]
            m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
            for _, row in Ristoranti_Quartiere.iterrows():
                folium.Marker( 
                    location=[row["LAT_WGS84"], row["LONG_WGS84"]],
                    popup=row['denominazione_pe'],
                    icon=folium.map.Icon(color='lightblue')
                ).add_to(m)
            for _, r in Quartiere_Trovato.iterrows():
                sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.0001)
                geo_j = sim_geo.to_json()
                geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
                folium.Popup(r['NIL']).add_to(geo_j)
                geo_j.add_to(m)
            return m._repr_html_()
        else:            
            return render_template("Progetto_Finale/Errore.html",Errore = Quartiere)
    else:
            return render_template("Progetto_Finale/Errore.html",Errore = Ristorante)
    

@app.route('/Mappa_Ristoranti_Municipio', methods=['GET'])
def Mappa_Ristoranti_Municipio():
    Ristorante = request.args['Ristorante'].lower()
    Municipio = request.args['Municipio']
    Municipio = int(Municipio)
    Ristoranti1 = Ristoranti.dropna()
    Ristoranti2=Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Ristorante)]['denominazione_pe'].to_list()
    if len(Ristoranti2) != 0:
        if Municipio in list(Ristoranti1['MUNICIPIO'].astype('int64')):           
            Ristoranti['MUNICIPIO'] = Ristoranti['MUNICIPIO'].dropna().astype('int64')
            Ristoranti_Trovato = Ristoranti1[Ristoranti1['denominazione_pe'].str.contains(Ristorante)]
            Municipio_Trovato = Municipi[Municipi['MUNICIPIO'] == Municipio]
            Ristoranti_Municipio = Ristoranti_Trovato[Ristoranti_Trovato.intersects(Municipio_Trovato.unary_union)]
            m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
            for _, row in Ristoranti_Municipio.iterrows():
                folium.Marker( 
                    location=[row["LAT_WGS84"], row["LONG_WGS84"]],
                    popup=row['denominazione_pe'],
                    icon=folium.map.Icon(color='lightblue')
                ).add_to(m)
            for _, r in Municipio_Trovato.iterrows():
                sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.0001)
                geo_j = sim_geo.to_json()
                geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red'})
                folium.Popup(r['MUNICIPIO']).add_to(geo_j)
                geo_j.add_to(m)
            return m._repr_html_()
        else:            
            return render_template("Progetto_Finale/Errore.html",Errore = Municipio)
    else:
            return render_template("Progetto_Finale/Errore.html",Errore = Ristorante)

# Login e Register
#@app.route('/Login', methods=['POST', 'GET']) 
#def  Login() : 
#    return render_template( 'Progetto_Finale/Login.html' )
   
#@app.route('/Controllo', methods=['Post']) 
#def  Controllo() : 
#
#    Dati_Utenti = pd.read_csv('/workspace/Flask/templates/Progetto_Finale/Dati_Utenti.csv')
#    Dati_Utente = {'Nome':Nome_Utente,'Password':Password}
#    Dati_Utenti = Dati_Utenti.append(Dati_Utente,ignore_index=True)
#    if request.method == 'POST':
#        Nome_Utente = request.form('nm')
#        Password = request.form('Password')
#        if Nome_Utente in Dati_Utente['Nome']:
#            if Password in Dati_Utente['Password']:
#                return render_template( 'Progetto_Finale/link_Pr.html' )
#            else:
#                return render_template("Progetto_Finale/Errore.html",Errore = 'Password')
#        else:
#            return render_template("Progetto_Finale/Errore.html",Errore = 'Nome_Utente')

# l'utente inserisce il nome del ristorante e trova gli occupazioni di  quel municipio
@app.route('/Cerca_Nome_Ristorante', methods=['GET'])
def Cerca_Nome_Ristorante():
    Nome_Ristoranti = Ristoranti.drop_duplicates(subset='insegna').dropna().sort_values('insegna').reset_index()
    return render_template("Progetto_Finale/Cerca_Nome_Ristorante.html",Nome_Ristoranti = Nome_Ristoranti[['insegna']].to_html())

@app.route('/Mappa_Nome_Ristorante', methods=['GET'])
def Mappa_Nome_Ristorante():
    Nome = request.args['Nome']
    if Nome in list(Ristoranti['insegna']):
        Nome_Trovato = Ristoranti[Ristoranti['insegna'] == Nome]
        m = folium.Map(location=[45.500085,9.234780], zoom_start=12)
        for _, row in Nome_Trovato.iterrows():
            folium.Marker(
                location=[row["LAT_WGS84"], row["LONG_WGS84"]],
                popup=row[['insegna','denominazione_pe']],
                icon=folium.map.Icon(color='lightblue')
            ).add_to(m)
        
        return m._repr_html_()
    else:
        return render_template("Progetto_Finale/Errore.html",Errore = Nome)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)