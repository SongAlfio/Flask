#esercizio: visualizzare un server web che visualizzi l'ora e colori, lo sfondo in base all'orario: un colore per la mattina, uno per il pomeriggio, uno per la sera, uno per la note
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])#è il home page
def Orario():
    import datetime
    orario = datetime.datetime.now()
    return render_template("Orario.html",testo=orario)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)