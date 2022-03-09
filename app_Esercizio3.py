#realizzare un server web che permetta di conoscere capoluoghi di regione.
#l'utente inserisce il  nome della regione e il programma restituisce il nome del capoluogo della regione.
#caricare i capoluoghi di regione in una opportuna struttura dati(lista di dizionario).

#modificare poi l'esercizio precedente per permettere all'utente di inseruire un capoluogo e di avere la regione in qui si trova.
#l'utente sceglie se avere la regione o il capoluogo selezionando su un radio button.
from flask import Flask, render_template,request
app = Flask(__name__)
lista = []
geografia = {'Abruzzo': 'LAquila', 'Basilicata': 'Potenza', 'Calabria': 'Catanzaro', 'Campania': 'Napoli', 'Emilia-Romagna': 'Bologna', 'Friuli-Venezia Giulia': 'Trieste', 'Lazio': 'Roma', 'Liguria': 'Genova', 'Lombardia': 'Milano', 'Marche': 'Ancona', 'Molise': 'Campobasso', 'Piemonte': 'Torino', 'Puglia': 'Bari', 'Sardegna': 'Cagliari', 'Sicilia': 'Palermo', 'Toscana': 'Firenze', 'Trentino-Alto-Adige': 'Trento', 'Umbria': 'Perugia', 'Vale dAosta': 'Aosta', 'Veneto': 'Venezia'}

@app.route('/', methods=['GET'])
def home():
    return render_template("Form3.html")

@app.route('/dati', methods=['GET'])
def Regione():
    Regione = request.args['Regione']
    capoluogo = geografia[Regione]
    return capoluogo
    lista.append({'Regione':Regione, 'Capoluogo':capoluogo)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)