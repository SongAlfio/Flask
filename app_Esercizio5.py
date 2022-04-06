#si vuole realizzare un sito web per memorizzare le squadre di uno sport a scelta. l'utente deve poter inserire il nome della squadra e la data di fondazione e la città.
#detto in oltre poter effetuare delle ricerche inserendo uno delle valori nelle colonne e ottenendo i dati presenti.
#gestire i dati in un dataframe, e salvare su un file csv

from flask import Flask, render_template,request
app = Flask(__name__)
import pandas as pd

df1 = pd.DataFrame()
@app.route('/', methods=['GET'])
def home():
    return render_template('app_Esercizio5/Form5.html')

@app.route('/inserisci', methods=['GET'])
def inserisci():
    return render_template('app_Esercizio5/inserisci_Es5.html')

@app.route('/dati', methods=['GET'])
def dati():
    # inserimento dei dati nel file csv
    # lettura dei dati dal form html 
    squadra = request.args['Squadra']
    anno = request.args['Anno']
    citta = request.args['Citta']
    # lettura dei dati daal file nel dataframe
    df1 = pd.read_csv('/workspace/Flask/templates/dati.csv')
    # aggiungiamo i nuovi dati nel dataframe 
    nuovi_dati = {'squadra':squadra,'anno':anno,'citta':citta}
    
    df1 = df1.append(nuovi_dati,ignore_index=True)
    # salviamo il dataframe sul file dati.csv
    df1.to_csv('/workspace/Flask/templates/dati.csv', index=False)
    return df1.to_html()

@app.route('/ricerca', methods=['GET'])
def ricerca():
    return render_template('app_Esercizio5/ricerca_Es5.html')

@app.route('/dati1', methods=['GET'])
def dati1():
    Cerca = request.args['Ricerca']
    Elemento = request.args['Cerca']
    df1 = pd.read_csv('/workspace/Flask/templates/app_Esercizio5/dati.csv')
    df2 = df1[df1[Cerca]==Elemento]
    return df2.to_html()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)