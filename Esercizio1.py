from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("Esercizio1.html")

@app.route('/meteo', methods=['GET'])
def Meteo():
    return render_template("Esercizio1_meteo.html")

@app.route('/frase', methods=['GET'])
def Frase():
    return render_template("Esercizio1_frase.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)