#si vuole analizzare un sito web che permetta di visualizzare alcune informazioni sull’andamento dell’epidemia di covid nel nostro paese a partire dai dati presenti nel file
#l’utente sceglie la regione da un elenco (menù a tendina), clicca su un bottone e il sito deve visualizzare una tabella contenente relativa alla situazione di quel regione
#i dati da inserire nel menù a tendina devono essere caricati automaticamente dalla pagina

from flask import Flask, render_template,request
import pandas as pd
from pandas import DataFrame, read_csv;
app = Flask(__name__)

url = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-addizionale-booster.csv"
df = pd.read_csv(url)
df.to_html(header="true", table_id="table")
@app.route('/', methods=['GET'])
def home():
    reg = df['nome_area'].drop_duplicates().to_list()
    return render_template("app_Esercizio4/Form4.html",reg=reg)

@app.route('/dati', methods=['GET'])
def covid19():
    Regione = request.args['Regione']
    df1 = df[df['nome_area']==Regione]
    return render_template('app_Esercizio4/Pandas.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)