from flask import Flask, render_template
import random as rd
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("Esercizio1.html")

@app.route('/meteo', methods=['GET'])
def Meteo():
    n = rd.randint(0, 8)
    if n <= 2:
      previsione = 'pioggia'
      tempo = 'pioggia'
    else:
      if n >= 3 & n < 5:
        previsione = 'nuvoloso'
        tempo = 'nuvoloso'
      if n > 5:
        previsione = 'sole'
        tempo = 'sole'
    return render_template("Esercizio1_meteo.html", pr=previsione, tempo=tempo)


@app.route('/frasicelebri', methods=['GET'])
def Frase():
    return render_template("Esercizio1_frase.html")

@app.route('/quantomanca', methods=['GET'])
def Calendario():
    return render_template("Esercizio1_calendario.html")    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)