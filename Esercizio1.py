from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("Esercizio1.html")

@app.route('/Meteo', methods=['GET'])
def Meteo():
    return ('<h1>Ciao,Mondo!</h1>')

@app.route('/fr', methods=['GET'])
def bonjour():
    return ('<h1>Bonjour,Monde!</h1>')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)