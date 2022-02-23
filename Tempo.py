#esercizio: visualizzare un server web che visualizzi l'ora e colori, lo sfondo in base all'orario: un colore per la mattina, uno per il pomeriggio, uno per la sera, uno per la note
from flask import Flask, render_template#Render template è usato per chiamare la cartella template
app = Flask(__name__)
import datetime


@app.route('/')
def hello_world():
  minuti = datetime.datetime.now().minute
  if minuti%2==0:
    col='Green'
  else:
    col='Red'
  return render_template('Risposta.html',colore=col,min = minuti)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)