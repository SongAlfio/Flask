#si vuole realizzare un sito web per memorizzare le squadre di uno sport a scelta. l'utente deve poter inserire il nome della squadra e la data di fondazione e la città.
#detto in oltre poter effetuare delle ricerche inserendo uno delle valori nelle colonne e ottenendo i dati presenti.
#gestire i dati in un dataframe, e salvare su un file csv

from flask import Flask, render_template,request
import pandas as pd
from pandas import DataFrame, read_csv;
app = Flask(__name__)

df = pd.DataFrame([])
df.to_html(header="true", table_id="table")
@app.route('/', methods=['GET'])
def home():
    return render_template("Form5.html")

@app.route('/dati', methods=['GET'])
def squadre():
    Team_name = request.args['Tname']
    Fondazione = request.args['Year']
    Citta = request.args['City']
    df = df.append({'Team_name' : Team_name , 'Fondazione' : Fondazione, 'Città' : Citta} , ignore_index=True)

    return render_template("Pandas.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)