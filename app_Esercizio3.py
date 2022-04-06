#realizzare un server web che permetta di conoscere capoluoghi di regione.
#l'utente inserisce il  nome della regione e il programma restituisce il nome del capoluogo della regione.
#caricare i capoluoghi di regione in una opportuna struttura dati(lista di dizionario).

#modificare poi l'esercizio precedente per permettere all'utente di inseruire un capoluogo e di avere la regione in qui si trova.
#l'utente sceglie se avere la regione o il capoluogo selezionando su un radio button.
from flask import Flask, render_template,request
app = Flask(__name__)
lista = []
geografia = {
'Abruzzo': 'LAquila', 
'Basilicata': 'Potenza', 
'Calabria': 'Catanzaro', 
'Campania': 'Napoli', 
'Emilia-Romagna': 'Bologna', 
'Friuli-Venezia Giulia': 'Trieste',
'Lazio': 'Roma', 
'Liguria': 'Genova', 
'Lombardia': 'Milano', 
'Marche': 'Ancona', 
'Molise': 'Campobasso', 
'Piemonte': 'Torino', 
'Puglia': 'Bari', 
'Sardegna': 'Cagliari', 
'Sicilia': 'Palermo', 
'Toscana': 'Firenze', 
'Trentino-Alto-Adige': 'Trento', 
'Umbria': 'Perugia', 
'Vale dAosta': 'Aosta', 
'Veneto': 'Venezia'
}
key_list=list(geografia.keys())
value_list=list(geografia.values())

@app.route('/', methods=['GET'])
def home():
    return render_template("app_Esercizio3/Form3.html")

@app.route('/dati', methods=['GET'])
def Luogo():
    Luogo = request.args['Luogo']
    scelta = request.args['luogo']
    if scelta == 'C':
        for Regione in range(len(geografia)) :
            if Luogo == key_list[Regione]:
                capoluogo = value_list[Regione]
                return capoluogo
                lista.append({'Regione':Luogo, 'Capoluogo':capoluogo})
                print(lista)
    else:
        for Capoluogo in range(len(geografia)) :
            if Luogo == value_list[Capoluogo]:
                regione = key_list[Capoluogo]
                return regione
                lista.append({'Regione':Luogo, 'Capoluogo':regione})
                print(lista)
            
    


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)